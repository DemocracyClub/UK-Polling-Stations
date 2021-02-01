import json
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView

import boto3
from boto.pyami.config import Config
from botocore.exceptions import ClientError
from marshmallow import Schema, fields, validate
from marshmallow import ValidationError as MarshmallowValidationError

from councils.models import Council
from .models import File, Upload


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


def get_s3_client():
    config = Config()
    access_key = config.get_value(settings.BOTO_SECTION, "aws_access_key_id")
    secret_key = config.get_value(settings.BOTO_SECTION, "aws_secret_access_key")
    return boto3.client(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )


class RequireStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff


logger = logging.getLogger(__name__)


class FileUploadView(RequireStaffMixin, TemplateView):
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
            logger.error(f"{e}\n{body}")

            raise DjangoValidationError("Request body did not match schema")

        files = body["files"]
        if len(files) == 2 and files[0]["name"] == files[1]["name"]:
            raise DjangoValidationError("Files must have different names")

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
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

        resp = {"files": []}
        for f in body["files"]:
            bucket_name = settings.S3_UPLOADS_BUCKET
            object_name = f"{self.kwargs['gss']}/{now}/{f['name']}"
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
                Upload.objects.get_or_create(gss=council, timestamp=now)
            except ClientError:
                return JsonResponse(
                    {"error": "Could not authorize request"}, status=400
                )
        return JsonResponse(resp, status=200)


class CouncilView:
    def get_queryset(self):
        uploads = Upload.objects.all().order_by("-timestamp")
        qs = (
            Council.objects.all()
            .exclude(council_id__startswith="N09")
            .order_by("name")
            .prefetch_related(Prefetch("upload_set", uploads))
            .prefetch_related("upload_set__file_set")
        )
        return qs


class CouncilListView(RequireStaffMixin, CouncilView, ListView):
    template_name = "file_uploads/council_list.html"


class CouncilDetailView(RequireStaffMixin, CouncilView, DetailView):
    template_name = "file_uploads/council_detail.html"


class FileDetailView(RequireStaffMixin, DetailView):
    template_name = "file_uploads/file_detail.html"
    model = File
