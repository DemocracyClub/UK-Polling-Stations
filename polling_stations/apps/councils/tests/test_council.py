import datetime

from councils.models import Council
from councils.tests.factories import CouncilFactory
from data_importers.event_types import DataEventType
from data_importers.models import DataEvent, DataQuality
from data_importers.tests.factories import DataEventFactory
from django.test import TestCase
from django.utils import timezone
from file_uploads.tests.factories import UploadFactory
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
        PollingStationFactory(council=nwp_council)
        self.stations_council = CouncilFactory(
            council_id="MNO", name="With Stations Council"
        )
        PollingStationFactory(council=self.stations_council)
        DataEventFactory(
            council=nwp_council,
            created=timezone.now() - datetime.timedelta(minutes=20),
            event_type=DataEventType.TEARDOWN,
        )
        DataEventFactory(
            council=nwp_council,
            created=timezone.now() - datetime.timedelta(minutes=15),
            event_type=DataEventType.IMPORT,
        )
        DataEventFactory(
            council=nwp_council,
            created=timezone.now() - datetime.timedelta(minutes=10),
            event_type=DataEventType.TEARDOWN,
            metadata={"test_id": 21},
        )
        DataEventFactory(
            council=nwp_council,
            created=timezone.now() - datetime.timedelta(minutes=5),
            event_type=DataEventType.IMPORT,
            upload=UploadFactory(gss=nwp_council, github_issue="MySpecialIssue"),
            metadata={"test_id": 42},
        )

        self.no_stations_council = CouncilFactory(
            council_id="JKL", name="No Stations Council"
        )

    def test_nation(self):
        newport = Council.objects.get(pk="NWP")
        self.assertEqual("Wales", newport.nation)

    def test_with_polling_stations_in_db_qs(self):
        self.assertEqual(len(Council.objects.all()), 3)
        self.assertEqual(len(Council.objects.with_polling_stations_in_db()), 2)

    def test_has_polling_stations_in_db(self):
        self.assertTrue(self.stations_council.has_polling_stations_in_db)
        self.assertFalse(self.no_stations_council.has_polling_stations_in_db)

    def test_latest_data_event(self):
        self.assertEqual(
            set(DataEvent.objects.all().values_list("council_id", flat=True)), {"NWP"}
        )
        nwp_council = Council.objects.get(council_id="NWP")
        self.assertEqual(
            nwp_council.latest_data_event(DataEventType.IMPORT).metadata["test_id"], 42
        )
        self.assertEqual(
            nwp_council.latest_data_event(DataEventType.TEARDOWN).metadata["test_id"],
            21,
        )

    def test_latest_data_event_no_events(self):
        self.assertIsNone(
            self.no_stations_council.latest_data_event(DataEventType.IMPORT)
        )

    def test_live_upload(self):
        nwp_council = Council.objects.get(council_id="NWP")
        self.assertEqual(nwp_council.live_upload.github_issue, "MySpecialIssue")

    def test_live_upload_no_stations(self):
        self.assertIsNone(self.no_stations_council.live_upload)

    def test_live_upload_just_import(self):
        just_import_council = CouncilFactory()
        DataEventFactory(
            council=just_import_council,
            event_type=DataEventType.IMPORT,
            upload=UploadFactory(
                gss=just_import_council,
                github_issue="There's no teardown just an import",
            ),
        )
        PollingStationFactory(council=just_import_council)
        self.assertEqual(
            just_import_council.live_upload.github_issue,
            "There's no teardown just an import",
        )

    def test_live_upload_just_teardown(self):
        just_teardown_council = CouncilFactory()
        DataEventFactory(
            council=just_teardown_council,
            event_type=DataEventType.TEARDOWN,
            upload=UploadFactory(
                gss=just_teardown_council,
                github_issue="There's no teardown just an import",
            ),
        )
        PollingStationFactory(council=just_teardown_council)
        self.assertIsNone(just_teardown_council.live_upload)

    def test_dataquality_report_created_on_council_creation(self):
        with self.assertRaises(DataQuality.DoesNotExist):
            DataQuality.objects.get(council_id="XYZ")
        council = CouncilFactory(council_id="XYZ")
        self.assertEqual(DataQuality.objects.get(council_id="XYZ").num_addresses, 0)
        DataQuality.objects.filter(council_id="XYZ").update(num_addresses=10)
        council.name = "changed"
        council.save()
        self.assertEqual(1, len(DataQuality.objects.filter(council_id="XYZ")))
        self.assertEqual(DataQuality.objects.get(council_id="XYZ").num_addresses, 10)
