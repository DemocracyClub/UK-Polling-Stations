from django.core.management.base import BaseCommand
from file_uploads.models import UploadQuerySet


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        qs = UploadQuerySet.pending_upload_qs(self)
        if len(qs) == 0:
            pass
        else:
            for upload in qs:
                upload.send_error_email()
        return qs
