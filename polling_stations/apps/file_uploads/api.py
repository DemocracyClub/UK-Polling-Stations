from django.db import transaction
from rest_framework import serializers, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import File, Upload
from polling_stations.db_routers import get_principal_db_name

DB_NAME = get_principal_db_name()


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("csv_valid", "csv_rows", "csv_encoding", "ems", "key", "errors")


class UploadSerializer(serializers.ModelSerializer):
    file_set = FileSerializer(many=True)

    class Meta:
        model = Upload
        fields = ("gss", "timestamp", "github_issue", "file_set", "election_date")

    @transaction.atomic(using=DB_NAME)
    def create(self, validated_data):
        def update_file_set(validated_data):
            upload = Upload.objects.get(
                gss=validated_data["gss"],
                timestamp=validated_data["timestamp"],
                election_date=validated_data["election_date"],
            )
            for f in validated_data["file_set"]:
                File.objects.create(upload=upload, **f)
            return upload

        existing_upload = Upload.objects.get(
            gss=validated_data["gss"],
            election_date=validated_data["election_date"],
            timestamp=validated_data["timestamp"],
        )
        existing_files = File.objects.filter(upload=existing_upload)
        if len(validated_data["file_set"]) > len(existing_files):
            # Only overwrite the old data with the new report
            # if the new one has more stuff in it
            existing_files.delete()
            upload = update_file_set(validated_data)
        else:
            # In the situation where we're processing multiple files
            # if there's already an upload and it has more files in it
            # than the new one we're trying to write, assume an
            # out-of-order delivery has happened (entirely possible)
            # and leave the existing data in place.
            upload = existing_upload

        file_set = upload.file_set

        if file_set.exists():
            if (
                file_set.first().ems == "Democracy Counts" and file_set.count() == 2
            ) or file_set.first().ems != "Democracy Counts":
                upload.github_issue = validated_data["github_issue"]
                upload.save()
                upload.make_pull_request()
                upload.send_confirmation_email()
        else:
            upload.send_error_email()
        return upload


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().prefetch_related("file_set")
    serializer_class = UploadSerializer
    http_method_names = ["post"]

    def create(self, request):
        # only users authenticated with a token associated
        # with a superuser account may perform this action
        if not request.user.is_superuser:
            raise PermissionDenied()

        return super().create(request)
