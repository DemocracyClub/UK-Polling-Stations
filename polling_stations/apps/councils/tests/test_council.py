import datetime

from councils.models import Council, UnsafeToDeleteCouncil
from councils.tests.factories import CouncilFactory
from data_importers.event_types import DataEventType
from data_importers.models import DataEvent, DataQuality
from data_importers.tests.factories import DataEventFactory
from django.test import TestCase
from django.utils import timezone
from file_uploads.tests.factories import UploadFactory
from pollingstations.models import PollingStation, VisibilityChoices
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

    def test_update_station_visibility_from_events_unpublished_no_election_dates(self):
        council = CouncilFactory()
        for i, event_type in enumerate([DataEventType.TEARDOWN, DataEventType.IMPORT]):
            DataEventFactory(
                council=council,
                event_type=event_type,
            )
        ps = PollingStationFactory(
            council=council, visibility=VisibilityChoices.PUBLISHED
        )
        for visibility_status in [
            VisibilityChoices.UNPUBLISHED,
            VisibilityChoices.PUBLISHED,
            VisibilityChoices.UNPUBLISHED,
        ]:
            DataEventFactory(
                council=council,
                event_type=DataEventType.SET_STATION_VISIBILITY,
                payload={
                    "internal_council_id": ps.internal_council_id,
                    "visibility": visibility_status,
                    "payload_version": 1,
                },
            )

        council.update_station_visibility_from_events(ps)
        ps.refresh_from_db()
        self.assertEqual(ps.visibility, VisibilityChoices.UNPUBLISHED)

    def test_update_station_visibility_from_events_published_no_election_dates(self):
        council = CouncilFactory()

        ps = PollingStationFactory(
            council=council, visibility=VisibilityChoices.PUBLISHED
        )
        for visibility_status in [
            VisibilityChoices.UNPUBLISHED,
            VisibilityChoices.PUBLISHED,
        ]:
            DataEventFactory(
                council=council,
                event_type=DataEventType.SET_STATION_VISIBILITY,
                payload={
                    "internal_council_id": ps.internal_council_id,
                    "visibility": visibility_status,
                    "payload_version": 1,
                },
            )
        council.update_station_visibility_from_events(ps)
        ps.refresh_from_db()
        self.assertEqual(ps.visibility, VisibilityChoices.PUBLISHED)

    def test_update_station_visibility_from_events_unpublished_election_date(self):
        """
        Station is created with unpublished and published event from 2023-05-04, and an unpublish event from 2024-05-02
        Method called with 2024 date
        Should be unpublished
        """
        council = CouncilFactory()
        for i, event_type in enumerate([DataEventType.TEARDOWN, DataEventType.IMPORT]):
            DataEventFactory(
                council=council,
                event_type=event_type,
            )
        ps = PollingStationFactory(
            council=council, visibility=VisibilityChoices.PUBLISHED
        )
        for visibility_status, date in [
            (VisibilityChoices.UNPUBLISHED, "2023-05-04"),
            (VisibilityChoices.PUBLISHED, "2023-05-04"),
            (VisibilityChoices.UNPUBLISHED, "2024-05-02"),
        ]:
            DataEventFactory(
                council=council,
                event_type=DataEventType.SET_STATION_VISIBILITY,
                election_dates=[date],
                payload={
                    "internal_council_id": ps.internal_council_id,
                    "visibility": visibility_status,
                    "payload_version": 1,
                },
            )

        council.update_station_visibility_from_events(ps, election_dates=["2024-05-02"])
        ps.refresh_from_db()
        self.assertEqual(ps.visibility, VisibilityChoices.UNPUBLISHED)

    def test_update_station_visibility_from_events_not_unpublished_election_date(self):
        """
        Station is created with unpublished and published event from 2023-05-04, and an unpublish event from 2024-05-02
        Method called with 2023 date
        Should be published
        """
        council = CouncilFactory()
        for i, event_type in enumerate([DataEventType.TEARDOWN, DataEventType.IMPORT]):
            DataEventFactory(
                council=council,
                event_type=event_type,
            )
        ps = PollingStationFactory(
            council=council, visibility=VisibilityChoices.PUBLISHED
        )
        for visibility_status, date in [
            (VisibilityChoices.UNPUBLISHED, "2023-05-04"),
            (VisibilityChoices.PUBLISHED, "2023-05-04"),
            (VisibilityChoices.UNPUBLISHED, "2024-05-02"),
        ]:
            DataEventFactory(
                council=council,
                event_type=DataEventType.SET_STATION_VISIBILITY,
                election_dates=[date],
                payload={
                    "internal_council_id": ps.internal_council_id,
                    "visibility": visibility_status,
                    "payload_version": 1,
                },
            )

        council.update_station_visibility_from_events(ps, election_dates=["2023-05-04"])
        ps.refresh_from_db()
        self.assertEqual(ps.visibility, VisibilityChoices.PUBLISHED)

    def test_update_station_visibility_from_events_not_unpublished_future_election_date(
        self,
    ):
        """
        Station is created with unpublished and published event from 2023-05-04, and an unpublish event from 2024-05-02
        Method called with 2025 date
        Should be published
        """
        council = CouncilFactory()
        for i, event_type in enumerate([DataEventType.TEARDOWN, DataEventType.IMPORT]):
            DataEventFactory(
                council=council,
                event_type=event_type,
            )
        ps = PollingStationFactory(
            council=council, visibility=VisibilityChoices.PUBLISHED
        )
        for visibility_status, date in [
            (VisibilityChoices.UNPUBLISHED, "2023-05-04"),
            (VisibilityChoices.PUBLISHED, "2023-05-04"),
            (VisibilityChoices.UNPUBLISHED, "2024-05-02"),
        ]:
            DataEventFactory(
                council=council,
                event_type=DataEventType.SET_STATION_VISIBILITY,
                election_dates=[date],
                payload={
                    "internal_council_id": ps.internal_council_id,
                    "visibility": visibility_status,
                    "payload_version": 1,
                },
            )

        council.update_station_visibility_from_events(ps, election_dates=["2025-05-01"])
        ps.refresh_from_db()
        self.assertEqual(ps.visibility, VisibilityChoices.PUBLISHED)

    def test_update_station_visibility_from_events_unpublished_election_dates(
        self,
    ):
        """
        DataEvent and Station both have list of dates with intersect
        """
        council = CouncilFactory()
        for i, event_type in enumerate([DataEventType.TEARDOWN, DataEventType.IMPORT]):
            DataEventFactory(
                council=council,
                event_type=event_type,
            )
        ps = PollingStationFactory(
            council=council, visibility=VisibilityChoices.PUBLISHED
        )

        DataEventFactory(
            council=council,
            event_type=DataEventType.SET_STATION_VISIBILITY,
            election_dates=["2024-05-15", "2024-05-02"],
            payload={
                "internal_council_id": ps.internal_council_id,
                "visibility": VisibilityChoices.UNPUBLISHED,
                "payload_version": 1,
            },
        )

        council.update_station_visibility_from_events(
            ps,
            election_dates=["2024-05-02", "2024-06-06"],
        )
        ps.refresh_from_db()
        self.assertEqual(ps.visibility, VisibilityChoices.UNPUBLISHED)

    def test_update_all_station_visibilities_from_events(self):
        council = CouncilFactory()
        for i, event_type in enumerate([DataEventType.TEARDOWN, DataEventType.IMPORT]):
            DataEventFactory(
                council=council,
                event_type=event_type,
            )
        PollingStationFactory.create_batch(
            4, council=council, visibility=VisibilityChoices.PUBLISHED
        )
        for station in PollingStation.objects.filter(council=council)[:3]:
            DataEventFactory(
                council=council,
                event_type=DataEventType.SET_STATION_VISIBILITY,
                payload={
                    "internal_council_id": station.internal_council_id,
                    "visibility": VisibilityChoices.UNPUBLISHED,
                    "payload_version": 1,
                },
            )

        self.assertEqual(
            len(
                PollingStation.objects.filter(
                    council=council, visibility=VisibilityChoices.UNPUBLISHED
                )
            ),
            0,
        )
        council.update_all_station_visibilities_from_events()
        self.assertEqual(
            len(
                PollingStation.objects.filter(
                    council=council, visibility=VisibilityChoices.UNPUBLISHED
                )
            ),
            3,
        )


class CouncilSafeDeleteTest(TestCase):
    def test_delete_single_council(self):
        council: Council = CouncilFactory(council_id="AAA")
        self.assertEqual(1, Council.objects.count())
        self.assertFalse(council.pollingstation_set.exists())
        council.delete()
        self.assertEqual(0, Council.objects.count())

    def test_delete_single_council_with_polling_stations(self):
        # make a council and some polling stations
        council: Council = CouncilFactory(council_id="AAA")
        PollingStationFactory.create_batch(4, council=council)

        # Assert they're connected and exist
        self.assertEqual(1, Council.objects.count())
        self.assertEqual(4, PollingStation.objects.count())
        self.assertTrue(council.pollingstation_set.exists())

        # Try to delete
        with self.assertRaises(UnsafeToDeleteCouncil):
            council.delete()

        # it hasn't worked
        self.assertEqual(1, Council.objects.count())
        self.assertEqual(4, PollingStation.objects.count())

        # delete with force_cascade
        summ, dic = council.delete(force_cascade=True)

        self.assertEqual(7, summ)
        self.assertEqual(
            {
                "councils.CouncilGeography": 1,
                "councils.Council": 1,
                "data_importers.DataQuality": 1,
                "pollingstations.PollingStation": 4,
            },
            dic,
        )

        # check it's worked - i.e. empty db
        self.assertEqual(0, Council.objects.count())
        self.assertEqual(0, PollingStation.objects.count())

    def test_delete_qs_no_stations(self):
        for i in "ABCD":
            CouncilFactory.create(council_id=f"{i * 3}")

        self.assertEqual(4, Council.objects.count())

        summ, dic = Council.objects.all().delete()

        self.assertEqual(12, summ)
        self.assertEqual(
            {
                "councils.CouncilGeography": 4,
                "councils.Council": 4,
                "data_importers.DataQuality": 4,
            },
            dic,
        )

        # check it's worked - i.e. empty db
        self.assertEqual(0, Council.objects.count())

    def test_delete_qs_with_stations(self):
        for i in "ABCD":
            CouncilFactory.create(council_id=f"{i * 3}")
        PollingStationFactory.create_batch(
            4, council=Council.objects.get(council_id="AAA")
        )
        PollingStationFactory.create_batch(
            2, council=Council.objects.get(council_id="BBB")
        )

        self.assertEqual(4, Council.objects.count())
        self.assertEqual(6, PollingStation.objects.count())

        # Try to delete
        with self.assertRaises(UnsafeToDeleteCouncil):
            Council.objects.all().delete()

        self.assertEqual(4, Council.objects.count())
        self.assertEqual(6, PollingStation.objects.count())

        summ, dic = Council.objects.all().delete(force_cascade=True)

        self.assertEqual(18, summ)
        self.assertEqual(
            {
                "councils.CouncilGeography": 4,
                "councils.Council": 4,
                "data_importers.DataQuality": 4,
                "pollingstations.PollingStation": 6,
            },
            dic,
        )

        # check it's worked - i.e. empty db
        self.assertEqual(0, Council.objects.count())
