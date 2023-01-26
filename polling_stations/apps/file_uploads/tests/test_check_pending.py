from django.core import mail
from django.conf import settings
from django.test import TestCase
from file_uploads.models import Upload
from councils.models import Council
from file_uploads.management.commands import check_pending
from freezegun import freeze_time


class TestCheckPending(TestCase):
    def setUp(self):
        self.council1 = Council.objects.create(
            council_id="E09000001",
            name="City of London Corporation",
        )
        self.council2 = Council.objects.create(
            council_id="E09000002",
            name="Westminster City Council",
        )

    @freeze_time("2021-04-01 13:00:00+00:00")
    # Find pending uploads lasting 20 minutes or more, email us and log the email as sent
    def test_handle_long_pending_upload(self):
        Upload.objects.create(
            gss=self.council1,
            election_date="2021-05-06",
            timestamp="2021-04-01 11:45:00+00:00",
        )
        Upload.objects.create(
            gss=self.council2,
            election_date="2021-05-06",
            timestamp="2021-04-01 11:46:00+00:00",
        )
        self.assertEqual(len(Upload.objects.all()), 2)
        self.assertEqual(Upload.objects.all()[0].warning_about_pending_sent, False)
        self.assertEqual(Upload.objects.all()[1].warning_about_pending_sent, False)
        qs = check_pending.Command().handle()
        self.assertEqual(len(qs), 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, "File upload failed")
        self.assertEqual(mail.outbox[1].subject, "File upload failed")
        self.assertEqual(
            mail.outbox[0].body,
            "File upload failure: 2021-04-01 11:45:00+00:00: City of London Corporation. Please investigate further.",
        )
        self.assertEqual(
            mail.outbox[1].body,
            "File upload failure: 2021-04-01 11:46:00+00:00: Westminster City Council. Please investigate further.",
        )
        self.assertEqual(mail.outbox[0].to, [settings.DEFAULT_FROM_EMAIL])
        self.assertEqual(mail.outbox[1].to, [settings.DEFAULT_FROM_EMAIL])
        self.assertEqual(Upload.objects.all()[0].warning_about_pending_sent, True)
        self.assertEqual(Upload.objects.all()[1].warning_about_pending_sent, True)

    @freeze_time("2021-04-01 12:05:00+00:00")
    # Don't email us regarding pending uploads that take less than 20 minutes
    def test_handle_short_pending_upload(self):
        self.assertEqual(len(Upload.objects.all()), 0)
        Upload.objects.create(
            gss=self.council2,
            election_date="2023-05-06",
            timestamp="2023-04-01 12:00:00+00:00",
        )
        self.assertEqual(len(Upload.objects.all()), 1)
        self.assertEqual(Upload.objects.first().warning_about_pending_sent, False)
        qs = check_pending.Command().handle()
        self.assertEqual(len(qs), 0)
        self.assertEqual(Upload.objects.first().warning_about_pending_sent, False)
        self.assertEqual(len(mail.outbox), 0)
