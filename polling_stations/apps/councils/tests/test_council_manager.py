import datetime

from councils.models import Council
from councils.tests.factories import CouncilFactory
from django.test import TestCase
from django.utils import timezone
from file_uploads.models import UploadStatusChoices
from file_uploads.tests.factories import FileFactory, UploadFactory
from pollingstations.tests.factories import PollingStationFactory


class CouncilTest(TestCase):
    def setUp(self):
        nwp_council = CouncilFactory(
            **{
                "council_id": "NWP",
                "electoral_services_address": "Newport City Council\nCivic Centre\nNewport\nSouth Wales",
                "electoral_services_email": "uvote@newport.gov.uk",
                "electoral_services_phone_numbers": ["01633 656656"],
                "electoral_services_postcode": "NP20 4UR",
                "electoral_services_website": "http://www.newport.gov.uk/_dc/index.cfm?fuseaction=electoral.homepage",
                "name": "Newport Council",
                "identifiers": ["W06000022"],
            }
        )
        self.stations_council = CouncilFactory(
            council_id="MNO", name="With Stations Council"
        )
        self.no_stations_council = CouncilFactory(
            council_id="JKL", name="No Stations Council"
        )

        PollingStationFactory(council=nwp_council)
        PollingStationFactory(council=self.stations_council)

    def test_with_polling_stations_in_db_qs(self):
        self.assertEqual(len(Council.objects.all()), 3)
        self.assertEqual(len(Council.objects.with_polling_stations_in_db()), 2)

    def test_has_polling_stations_in_db(self):
        self.assertTrue(self.stations_council.has_polling_stations_in_db)
        self.assertFalse(self.no_stations_council.has_polling_stations_in_db)

    def test_with_future_upload_status_one_valid(self):
        latest_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=1),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory(upload=latest_upload)

        older_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=2),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory(upload=older_upload, csv_valid=False)

        c1 = Council.objects.with_future_upload_details().get(
            pk=self.stations_council.pk
        )
        self.assertEqual(c1.latest_upload_id, latest_upload.id)
        self.assertEqual(c1.latest_upload_status, UploadStatusChoices.OK)

    def test_with_future_upload_status_two_valid(self):
        latest_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=1),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory.create_batch(2, upload=latest_upload)

        older_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=2),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory(upload=older_upload, csv_valid=False)

        c1 = Council.objects.with_future_upload_details().get(
            pk=self.stations_council.pk
        )
        self.assertEqual(c1.latest_upload_id, latest_upload.id)
        self.assertEqual(c1.latest_upload_status, UploadStatusChoices.OK)

    def test_with_future_upload_status_one_invalid(self):
        latest_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=1),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory(upload=latest_upload, csv_valid=False)

        older_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=2),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory(upload=older_upload)

        c1 = Council.objects.with_future_upload_details().get(
            pk=self.stations_council.pk
        )
        self.assertEqual(c1.latest_upload_id, latest_upload.id)
        self.assertEqual(c1.latest_upload_status, UploadStatusChoices.ERROR)

    def test_with_future_upload_status_one_valid_one_invalid(self):
        latest_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=1),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory(upload=latest_upload, csv_valid=False)
        FileFactory(upload=latest_upload, csv_valid=True)
        older_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=2),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        FileFactory(upload=older_upload)
        c1 = Council.objects.with_future_upload_details().get(
            pk=self.stations_council.pk
        )
        self.assertEqual(c1.latest_upload_id, latest_upload.id)
        self.assertEqual(c1.latest_upload_status, UploadStatusChoices.ERROR)

    def test_with_future_upload_status_no_upload(self):
        c2 = Council.objects.with_future_upload_details().get(
            pk=self.no_stations_council.pk
        )
        self.assertEqual(len(c2.upload_set.all()), 0)
        self.assertIsNone(c2.latest_upload_status)
        self.assertIsNone(c2.latest_upload_id)

    def test_with_future_upload_status_returns_all(self):
        self.assertEqual(len(Council.objects.with_future_upload_details()), 3)

    def test_with_future_upload_status_no_file(self):
        latest_upload = UploadFactory(
            gss=self.stations_council,
            timestamp=timezone.now() - datetime.timedelta(days=1),
            election_date=timezone.now().date() + datetime.timedelta(days=10),
        )
        c1 = Council.objects.with_future_upload_details().get(
            pk=self.stations_council.pk
        )
        self.assertEqual(c1.latest_upload_id, latest_upload.id)
        self.assertEqual(c1.latest_upload_status, UploadStatusChoices.PENDING)
