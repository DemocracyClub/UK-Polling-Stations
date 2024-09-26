import json
import logging
import os
from datetime import datetime

import boto3
from addressbase.models import Address, UprnToCouncil
from botocore.exceptions import ClientError
from councils.models import Council
from data_finder.helpers import EveryElectionWrapper
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import DEFAULT_DB_ALIAS
from django.db.models import Count, Max, Subquery
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.generic import DetailView, FormView, ListView, TemplateView
from file_uploads.forms import CouncilLoginForm, CSVUploadForm
from marshmallow import Schema, fields, validate
from marshmallow import ValidationError as MarshmallowValidationError
from pollingstations.models import (
    VisibilityChoices,
)
from sentry_sdk import capture_message
from sesame.utils import get_query_string, get_user

from .accessibility_information_handler import AccessibilityInformationHandler
from .filters import CouncilListUploadFilter
from .models import File, Upload
from .utils import assign_councils_to_user, get_domain

User = get_user_model()


class FileSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Regexp(
            r"(?i)^.+(\.csv|\.tsv)$", error="Unexpected file type"
        ),
    )
    size = fields.Integer(
        required=True,
        validate=validate.Range(
            min=0, max=settings.MAX_FILE_SIZE, error="File too big"
        ),
    )
    type = fields.String(required=False)


class UploadRequestSchema(Schema):
    files = fields.List(
        fields.Nested(FileSchema()),
        required=True,
        validate=validate.Length(min=1, max=2),
    )
    election_date = fields.Date(required=True)


def get_s3_client():
    return boto3.client("s3", region_name=os.environ.get("AWS_REGION", "eu-west-2"))


class CouncilFileUploadAllowedMixin(UserPassesTestMixin):
    def get_login_url(self):
        return reverse_lazy("file_uploads:council_login_view")

    def test_func(self):
        return self.request.user.is_active


logger = logging.getLogger(__name__)


class FileUploadView(CouncilFileUploadAllowedMixin, TemplateView):
    template_name = "file_uploads/upload.html"

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **context):
        context["council"] = (
            Council.objects.all()
            .exclude(council_id__startswith="N09")
            .get(council_id=self.kwargs["gss"])
        )
        upcoming_election_dates = EveryElectionWrapper(
            council_id=self.kwargs["gss"]
        ).get_future_election_dates()

        # If the list returns no items, flag that there are no upcoming elections
        # that we know about.
        context["NO_UPCOMING_ELECTIONS"] = bool(upcoming_election_dates)

        # Only show the date picker if there's more than one upcoming election date
        context["SHOW_DATE_PICKER"] = len(upcoming_election_dates) > 1

        context["UPCOMING_ELECTION_DATES"] = upcoming_election_dates

        return context

    def validate_body(self, body):
        """
        Do some basic picture checks on request body and files.
        Obviously these values can be spoofed, so checks on
        file extension and MIME type etc are just to "fail fast".
        We will check the files _properly_ in the lambda hook.
        """
        try:
            UploadRequestSchema().load(body)
        except MarshmallowValidationError as e:
            # for now, log the error and body to sentry
            # so we've got visibility on errors
            capture_message(f"{e}\n{body}", level="error")

            raise DjangoValidationError("Request body did not match schema")

        files = body["files"]
        if len(files) == 2 and files[0]["name"] == files[1]["name"]:
            raise DjangoValidationError("Files must have different names")

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """
        Expects a request matching the UploadRequestSchema
        Fetches, and returns, a presigned url for an s3 upload.
        This endpoint is called in templates/upload.html from the js,
        which then uses the presigned url to upload the users files.
        """
        body = json.loads(request.body)

        try:
            self.validate_body(body)
            try:
                council = Council.objects.get(pk=self.kwargs["gss"])
            except Council.DoesNotExist as e:
                raise DjangoValidationError(str(e))
        except DjangoValidationError as e:
            return JsonResponse({"error": e.message}, status=400)

        client = get_s3_client()
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        election_date = body["election_date"]

        resp = {"files": []}
        for f in body["files"]:
            bucket_name = settings.S3_UPLOADS_BUCKET
            object_name = f"{self.kwargs['gss']}/{election_date}/{now}/{f['name']}"
            fields = {"Content-Type": f["type"]}
            conditions = [
                {"Content-Type": f["type"]},
                ["content-length-range", 0, settings.MAX_FILE_SIZE],
            ]
            expiration = 600  # 10 mins
            try:
                resp["files"].append(
                    client.generate_presigned_post(
                        bucket_name,
                        object_name,
                        Fields=fields,
                        Conditions=conditions,
                        ExpiresIn=expiration,
                    )
                )
                Upload.objects.get_or_create(
                    gss=council,
                    election_date=election_date,
                    timestamp=now,
                    upload_user=request.user,
                )
            except ClientError:
                return JsonResponse(
                    {"error": "Could not authorize request"}, status=400
                )
        return JsonResponse(resp, status=200)


class CouncilView:
    def get_queryset(self):
        qs = (
            Council.objects.with_future_upload_details()
            .exclude(council_id__startswith="N09")
            .annotate(ps_count=Count("pollingstation"))
            .order_by("name")
        )
        if not self.request.user.is_staff:
            qs = qs.filter(usercouncils__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get("pk"):
            upcoming_election_dates = EveryElectionWrapper(
                council_id=self.kwargs["pk"]
            ).get_future_election_dates()
            context["HAS_UPCOMING_ELECTIONS"] = bool(upcoming_election_dates)
            context["NO_COUNCILS"] = False

        return context


class CouncilListView(CouncilFileUploadAllowedMixin, CouncilView, ListView):
    template_name = "file_uploads/council_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = CouncilListUploadFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        # Add the filter to the context
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        return context

    def get(self, request, *args, **kwargs):
        user_councils = self.get_queryset()
        if user_councils.count() == 1 and not request.user.is_staff:
            return redirect(
                reverse(
                    "file_uploads:councils_detail",
                    kwargs={"pk": user_councils.first().pk},
                )
            )
        return super().get(request, *args, **kwargs)


def get_station_to_example_uprn_map(council: Council) -> dict[str, dict[str, str]]:
    sample_uprn_per_station = (
        UprnToCouncil.objects.filter(lad=council.geography.gss)
        .exclude(polling_station_id="")
        .values("polling_station_id")
        .annotate(max_uprn=Max("uprn"))
    )
    address_list = Address.objects.filter(
        uprn__in=Subquery(sample_uprn_per_station.values("max_uprn"))
    ).values_list(
        "uprntocouncil__polling_station_id",
        "uprn",
        "postcode",
    )
    return {a[0]: {"uprn": a[1], "postcode": [a[2]]} for a in address_list}


def get_example_uprn(station, station_to_example_uprn_map):
    if station.internal_council_id in station_to_example_uprn_map:
        return station_to_example_uprn_map.get(station.internal_council_id).get(
            "uprn", None
        )
    return None


def get_example_postcode(station, station_to_example_uprn_map):
    if station.internal_council_id in station_to_example_uprn_map:
        return station_to_example_uprn_map.get(station.internal_council_id).get(
            "postcode", None
        )
    return None


class CouncilDetailView(CouncilFileUploadAllowedMixin, CouncilView, DetailView):
    template_name = "file_uploads/council_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["EC_COUNCIL_CONTACT_EMAIL"] = settings.EC_COUNCIL_CONTACT_EMAIL
        council = context["council"]
        council_from_default_db = Council.objects.using(DEFAULT_DB_ALIAS).get(
            council_id=council.council_id
        )
        context["STATIONS"] = []
        station_to_example_uprn_map = get_station_to_example_uprn_map(
            council_from_default_db
        )
        for station in council_from_default_db.pollingstation_set.all():
            context["STATIONS"].append(
                {
                    "address": station.address,
                    "postcode": station.postcode,
                    "location": "✔️" if station.location else "❌",
                    "example_uprn": get_example_uprn(
                        station, station_to_example_uprn_map
                    ),
                    "example_postcode": get_example_postcode(
                        station, station_to_example_uprn_map
                    ),
                    "visibility": VisibilityChoices[station.visibility].label,
                    "pk": station.id,
                }
            )
        context["STATIONS"].sort(key=lambda d: d["address"])
        context["live_upload"] = council.live_upload
        context["events"] = council.dataevent_set.all().order_by("-created")
        return context


class FileDetailView(CouncilFileUploadAllowedMixin, DetailView):
    template_name = "file_uploads/file_detail.html"
    model = File


class CouncilLoginView(FormView):
    form_class = CouncilLoginForm
    template_name = "file_uploads/council_login.html"

    def form_valid(self, form):
        """
        Create or retrieve a user trigger the send login email
        """
        user, created = User.objects.get_or_create(
            email=form.cleaned_data["email"],
            username=form.cleaned_data["email"],
        )
        if created:
            user.set_unusable_password()
            user.save()

        self.send_login_url(user=user)
        messages.success(
            self.request,
            "Thank you, please check your email for your magic link to log in to your account.",
            fail_silently=True,
        )
        return HttpResponseRedirect(self.get_success_url())

    def send_login_url(self, user):
        """
        Send an email to the user with a link to authenticate and log in
        """
        querystring = get_query_string(user=user)
        domain = get_domain(request=self.request)
        path = reverse("file_uploads:council_authenticate")
        url = f"{self.request.scheme}://{domain}{path}{querystring}"
        subject = "Your magic link to log in to the WhereDoIVote Uploader"
        txt = render_to_string(
            template_name="file_uploads/email/login_message.txt",
            context={
                "authenticate_url": url,
                "subject": subject,
            },
        )
        return user.email_user(subject=subject, message=txt)

    def get_success_url(self):
        """
        Redirect to same page where success message will be displayed
        """
        return reverse("file_uploads:council_login_view")


class AuthenticateView(TemplateView):
    template_name = "file_uploads/authenticate.html"

    def get(self, request, *args, **kwargs):
        """
        Attempts to get user from the request, log them in, and redirect them to
        their profile page. Renders an error message if django-sesame fails to
        get a user from the request.
        """
        token = self.request.GET.get("login_token")
        if not token:
            return redirect(reverse("file_uploads:council_login_view"))
        user = get_user(token)
        if not user:
            return super().get(request, *args, **kwargs)
        login(request, user, backend="sesame.backends.ModelBackend")
        assign_councils_to_user(user)
        return redirect("file_uploads:councils_list")


class AccessibilityInformationUploadView(UserPassesTestMixin, FormView):
    template_name = "file_uploads/upload_accessibility_information.html"
    form_class = CSVUploadForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.council = None

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        self.council: Council = Council.objects.prefetch_related(
            "pollingstation_set"
        ).get(council_id=self.kwargs["council_id"])
        uploaded_file = self.request.FILES["csv_file"]
        rows: list[str] = [
            line.decode("utf-8").replace("\n", "") for line in uploaded_file
        ]
        file_handler = AccessibilityInformationHandler(self.council)
        file_handler.handle(rows)
        if file_handler.errors:
            pass  # do stuff with errors
        if file_handler.infos:
            pass  # do stuff with infos

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "file_uploads:councils_detail", kwargs={"pk": self.council.council_id}
        )
