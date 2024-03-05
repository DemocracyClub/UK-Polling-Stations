from django.core.management.base import BaseCommand
from file_uploads.models import Upload


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        qs = Upload.objects.pending_upload_qs()
        if len(qs) == 0:
            pass
        else:
            for upload in qs:
                upload.send_error_email()
        return qs
