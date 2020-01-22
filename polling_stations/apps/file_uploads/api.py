from django.db import transaction
from rest_framework import serializers, viewsets
from rest_framework.exceptions import PermissionDenied
from .models import File, Upload


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("csv_valid", "csv_rows", "ems", "key", "errors")


class UploadSerializer(serializers.ModelSerializer):
    file_set = FileSerializer(many=True)

    class Meta:
        model = Upload
        fields = ("gss", "timestamp", "github_issue", "file_set")

    @transaction.atomic
    def create(self, validated_data):
        def save(validated_data):
            upload = Upload.objects.create(
                gss=validated_data["gss"],
                timestamp=validated_data["timestamp"],
                github_issue=validated_data["github_issue"],
            )
            for f in validated_data["file_set"]:
                File.objects.create(upload=upload, **f)
            return upload

        try:
            existing_upload = Upload.objects.get(
                gss=validated_data["gss"], timestamp=validated_data["timestamp"]
            )
            existing_files = File.objects.filter(upload=existing_upload)
            if len(validated_data["file_set"]) > len(existing_files):
                # Only overwrite the old data with the new report
                # if the new one has more stuff in it
                existing_files.delete()
                existing_upload.delete()
                return save(validated_data)
            else:
                # In the situation where we're processing multiple files
                # if there's already an upload and it has more files in it
                # than the new one we're trying to write, assume an
                # out-of-order delivery has happened (entirely possible)
                # and leave the existing data in place.
                return existing_upload
        except Upload.DoesNotExist:
            return save(validated_data)


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
