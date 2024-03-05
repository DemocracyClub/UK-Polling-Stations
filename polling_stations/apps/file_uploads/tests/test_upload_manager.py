import datetime

from django.test import TestCase
from django.utils import timezone
from file_uploads.models import Upload, UploadStatusChoices
from file_uploads.tests.factories import FileFactory, UploadFactory


class UploadManagerWithStatus(TestCase):
    def test_ok_one_file(self):
        ok_upload_one_file = UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(weeks=1),
        )
        FileFactory(
            upload_id=ok_upload_one_file.id,
        )
        self.assertEqual(
            Upload.objects.with_status().first().status, UploadStatusChoices.OK
        )

    def test_ok_two_files(self):
        ok_upload_two_file = UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(weeks=1),
        )
        FileFactory.create_batch(
            2,
            upload_id=ok_upload_two_file.id,
        )
        self.assertEqual(
            Upload.objects.with_status().first().status, UploadStatusChoices.OK
        )

    def test_error_upload_one_invalid_file(self):
        error_upload_one_invalid_file = UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(weeks=1),
        )
        FileFactory(upload_id=error_upload_one_invalid_file.id, csv_valid=False)
        self.assertEqual(
            Upload.objects.with_status().first().status,
            UploadStatusChoices.ERROR,
        )

    def test_error_upload_two_invalid_files(self):
        error_upload_two_invalid_files = UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(weeks=1),
        )
        FileFactory.create_batch(
            2, upload_id=error_upload_two_invalid_files.id, csv_valid=False
        )
        self.assertEqual(
            Upload.objects.with_status().first().status,
            UploadStatusChoices.ERROR,
        )

    def error_upload_one_valid_one_invalid(self):
        error_upload_one_valid_one_invalid = UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(weeks=1),
        )
        FileFactory(
            upload_id=error_upload_one_valid_one_invalid.id,
        )
        FileFactory(upload_id=error_upload_one_valid_one_invalid.id, csv_valid=False)
        self.assertEqual(
            Upload.objects.with_status().first().status,
            UploadStatusChoices.ERROR,
        )

    def test_error_one_file_upload(self):
        error_one_file_upload = UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(weeks=1),
        )
        FileFactory(
            upload_id=error_one_file_upload.id,
            csv_valid=False,
            errors="Expected 2 files, found 1",
        )
        self.assertEqual(
            Upload.objects.with_status().first().status,
            UploadStatusChoices.ERROR_ONE_FILE,
        )

    def test_waiting_second_file_upload(self):
        pending_upload = UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(seconds=90),
        )
        FileFactory(
            upload_id=pending_upload.id,
            csv_valid=False,
            errors="Expected 2 files, found 1",
        )
        self.assertEqual(
            Upload.objects.with_status().first().status,
            UploadStatusChoices.WAITING_SECOND_FILE,
        )

    def test_pending_upload(self):
        """
        A PENDING Upload is when the upload object exists, but no files exist
        """
        UploadFactory(
            election_date=timezone.now().date() + datetime.timedelta(weeks=4),
            timestamp=timezone.now() - datetime.timedelta(weeks=1),
        )

        self.assertEqual(
            Upload.objects.with_status().first().status,
            UploadStatusChoices.PENDING,
        )
