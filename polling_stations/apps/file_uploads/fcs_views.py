import datetime as dt
from urllib.parse import urljoin

import boto3
import requests

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils import timezone

from django.views.generic import TemplateView

from councils.models import Council
from data_finder.helpers.every_election import EEFetcher, EEWrapper

from .forms import ElectionDateForm, ElectionForm
from .mixins import StaffUserRequiredMixin
from .models import Upload


class FcsDateSelectView(StaffUserRequiredMixin, TemplateView):
    template_name = "file_uploads/fcs/date_select.html"

    def get_upcoming_election_dates(self):
        return EEWrapper(
            **EEFetcher(council_id=self.kwargs["council_id"]).fetch()
        ).get_future_election_dates()

    def get_context_data(self, form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        upcoming_election_dates = self.get_upcoming_election_dates()
        context["council"] = (
            Council.objects.all()
            .exclude(council_id__startswith="N09")
            .get(council_id=self.kwargs["council_id"])
        )
        context["NO_UPCOMING_DATES"] = not upcoming_election_dates
        context["UPCOMING_ELECTION_DATES"] = upcoming_election_dates
        context["form"] = form or ElectionDateForm(
            election_dates=upcoming_election_dates
        )
        return context

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if len(context["UPCOMING_ELECTION_DATES"]) == 1:
            return redirect(
                "file_uploads:fcs_election_select",
                council_id=context["council"].council_id,
                date=context["UPCOMING_ELECTION_DATES"][0],
            )
        return self.render_to_response(context)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        upcoming_election_dates = self.get_upcoming_election_dates()
        form = ElectionDateForm(request.POST, election_dates=upcoming_election_dates)
        if form.is_valid():
            return redirect(
                "file_uploads:fcs_election_select",
                council_id=self.kwargs["council_id"],
                date=form.cleaned_data["election_date"],
            )
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)


class FcsElectionSelectView(StaffUserRequiredMixin, TemplateView):
    template_name = "file_uploads/fcs/election_select.html"

    def get_elections_for_date(self, council, date):
        resp = requests.get(
            urljoin(council.fcscredential.url, "/api/DemocracyClub/Election/"),
            headers={
                "Accept": "*/*",
                "User-Agent": "Scraper/DemocracyClub",
                "X-API-KEY": council.fcscredential.token,
            },
        )
        resp.raise_for_status()
        elections = resp.json()
        # The FCS API returns election dates as UTC datetimes in ISO format
        # so we need to convert them to local dates before comparing with the requested date
        requested_date = dt.date.fromisoformat(date)
        return [
            e
            for e in elections
            if timezone.localdate(dt.datetime.fromisoformat(e["electionDate"]))
            == requested_date
        ]

    def get_context_data(self, form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["council"] = (
            Council.objects.all()
            .exclude(council_id__startswith="N09")
            .get(council_id=self.kwargs["council_id"])
        )
        elections_for_date = self.get_elections_for_date(
            context["council"], kwargs["date"]
        )
        context["NO_UPCOMING_ELECTIONS"] = not elections_for_date
        context["ELECTIONS_FOR_DATE"] = elections_for_date
        context["form"] = form or ElectionForm(elections=elections_for_date)
        return context

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if len(context["ELECTIONS_FOR_DATE"]) == 1:
            election = context["ELECTIONS_FOR_DATE"][0]
            return redirect(
                "file_uploads:fcs_snapshot_data",
                council_id=context["council"].council_id,
                date=self.kwargs["date"],
                election_id=election["id"],
            )
        return self.render_to_response(context)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        council = (
            Council.objects.all()
            .exclude(council_id__startswith="N09")
            .get(council_id=self.kwargs["council_id"])
        )
        elections_for_date = self.get_elections_for_date(council, self.kwargs["date"])
        form = ElectionForm(request.POST, elections=elections_for_date)
        if form.is_valid():
            return redirect(
                "file_uploads:fcs_snapshot_data",
                council_id=self.kwargs["council_id"],
                date=self.kwargs["date"],
                election_id=form.cleaned_data["election_id"],
            )
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)


class FcsSnapshotDataView(StaffUserRequiredMixin, TemplateView):
    template_name = "file_uploads/fcs/snapshot_data.html"

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        council = (
            Council.objects.all()
            .exclude(council_id__startswith="N09")
            .select_related("fcscredential")
            .get(council_id=self.kwargs["council_id"])
        )

        election_date = kwargs["date"]
        # validate
        dt.datetime.strptime(election_date, "%Y-%m-%d")

        election_id = kwargs["election_id"]

        now = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

        # acquire lock
        # https://github.com/DemocracyClub/UK-Polling-Stations/pull/9552#discussion_r3706676826
        cache_key = f"fcslock-{council.council_id}-{election_date}"
        if cache.get(cache_key):
            messages.error(
                self.request, "snapshot already in progress - refresh page in 1 minute"
            )
            return redirect(
                reverse("file_uploads:councils_detail", kwargs={"pk": council.pk}),
            )
        else:
            cache.set(cache_key, True, timeout=40)

        try:
            resp = requests.get(
                urljoin(
                    council.fcscredential.url,
                    f"/api/DemocracyClub/Election/{election_id}/PollingStation",
                ),
                headers={
                    "Accept": "*/*",
                    "User-Agent": "Scraper/DemocracyClub",
                    "X-API-KEY": council.fcscredential.token,
                },
            )

            resp.raise_for_status()

            conn = boto3.client("s3")
            conn.put_object(
                Bucket=settings.S3_UPLOADS_BUCKET,
                Key=f"{council.council_id}/{election_date}/{now}/snapshot.json",
                Body=resp.text,
            )

            Upload.objects.create(
                gss=council,
                election_date=kwargs["date"],
                timestamp=now,
                upload_user=request.user,
            )
        finally:
            # unlock
            cache.delete(cache_key)

        return redirect(
            reverse("file_uploads:councils_detail", kwargs={"pk": council.pk}),
        )
