from councils.tests.factories import CouncilFactory
from data_importers.event_helpers import (
    EventValidationError,
    record_teardown_event,
    set_station_field_from_event,
    set_station_visibility,
)
from data_importers.event_types import (
    DataEventType,
    EventUserType,
    StationCorrectionSource,
)
from data_importers.models import DataEvent
from data_importers.tests.factories import DataEventFactory
from django.test import TestCase
from pollingstations.models import VisibilityChoices
from pollingstations.tests.factories import PollingStationFactory


class CouncilTest(TestCase):
    def setUp(self):
        self.nwp_council = CouncilFactory(
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

    def test_record_teardown_event(self):
        self.assertEqual(len(DataEvent.objects.all()), 0)
        record_teardown_event(self.nwp_council.council_id)
        self.assertEqual(
            len(
                DataEvent.objects.filter(
                    event_type=DataEventType.TEARDOWN,
                    council=self.nwp_council,
                )
            ),
            1,
        )
        self.assertEqual(len(DataEvent.objects.all()), 1)


class PollingStationEventTest(TestCase):
    def setUp(self):
        CouncilFactory(council_id="ABC")
        self.station = PollingStationFactory(
            internal_council_id="32A",
            address="Village Hall\nWinklesford Merriot",
            postcode="FOOBAR",
            council_id="ABC",
        )
        self.unpublish_event = DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.SET_STATION_VISIBILITY,
            payload={
                "internal_council_id": "32A",
                "visibility": VisibilityChoices.UNPUBLISHED,
                "payload_version": 1,
            },
            metadata={
                "reason": StationCorrectionSource.DEMOCRACY_CLUB,
                "reason_detail": "Station address is wrong",
                "source": EventUserType.ADMIN,
            },
        )
        self.publish_event = DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.SET_STATION_VISIBILITY,
            payload={
                "internal_council_id": "32A",
                "visibility": VisibilityChoices.PUBLISHED,
                "payload_version": 1,
            },
            metadata={
                "reason": StationCorrectionSource.DEMOCRACY_CLUB,
                "reason_detail": "All ok!",
                "source": EventUserType.ADMIN,
            },
        )

    def test_set_station_visibility(self):
        # Make check station is published
        self.assertEqual(self.station.visibility, VisibilityChoices.PUBLISHED)

        # replay unpublish event
        set_station_visibility(self.unpublish_event)
        # refresh station from db
        self.station.refresh_from_db()
        # Check station is unpublished
        self.assertEqual(self.station.visibility, VisibilityChoices.UNPUBLISHED)

        # Do the same, but the other way:
        # Replay publish event
        set_station_visibility(self.publish_event)
        # refresh station from db
        self.station.refresh_from_db()
        # Check station is unpublished
        self.assertEqual(self.station.visibility, VisibilityChoices.PUBLISHED)

    def test_set_station_field_from_event(self):
        # Make check station is published
        self.assertEqual(self.station.visibility, VisibilityChoices.PUBLISHED)

        # replay unpublish event
        set_station_field_from_event(self.unpublish_event)
        # refresh station from db
        self.station.refresh_from_db()
        # Check station is unpublished
        self.assertEqual(self.station.visibility, VisibilityChoices.UNPUBLISHED)
        # Do the same, but the other way:
        # Replay publish event
        set_station_field_from_event(self.publish_event)
        # refresh station from db
        self.station.refresh_from_db()
        # Check station is unpublished
        self.assertEqual(self.station.visibility, VisibilityChoices.PUBLISHED)

    def test_set_station_visibility_payload_missing_visibility(self):
        event_missing_visibility = DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.SET_STATION_VISIBILITY,
            payload={
                "internal_council_id": "32A",
                "payload_version": 1,
            },
        )
        with self.assertRaises(EventValidationError) as e:
            set_station_visibility(event_missing_visibility)
        self.assertEqual(
            str(e.exception),
            f"DataEvent object ({event_missing_visibility.pk}) payload missing visibility.",
        )

    def test_set_station_visibility_invalid_visibility(self):
        event_invalid_visibility = DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.SET_STATION_VISIBILITY,
            payload={
                "internal_council_id": "32A",
                "visibility": ("HIDDEN", "Hidden"),
                "payload_version": 1,
            },
        )
        with self.assertRaises(EventValidationError) as e:
            set_station_visibility(event_invalid_visibility)
        self.assertEqual(
            str(e.exception),
            f"DataEvent visibility not a valid choice. Visibility was '('HIDDEN', 'Hidden')', choices are {VisibilityChoices.choices}.",
        )

    def test_set_station_field_wrong_event_type(self):
        import_event = DataEventFactory(
            council_id="ABC", event_type=DataEventType.IMPORT
        )
        with self.assertRaises(EventValidationError) as e:
            set_station_field_from_event(import_event)
        self.assertEqual(
            str(e.exception),
            f"{import_event} event_type ('IMPORT') does not appear in DataEventType.station_update_event_types",
        )

    def test_set_station_field_missing_station_id(self):
        event_missing_station_id = DataEventFactory(
            council_id="ABC",
            event_type=DataEventType.SET_STATION_VISIBILITY,
            payload={
                "visibility": VisibilityChoices.UNPUBLISHED,
                "payload_version": 1,
            },
        )
        with self.assertRaises(EventValidationError) as e:
            set_station_field_from_event(event_missing_station_id)
        self.assertEqual(
            str(e.exception), f"{event_missing_station_id} payload missing station id."
        )
