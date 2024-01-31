from councils.tests.factories import CouncilFactory
from data_importers.event_helpers import record_teardown_event
from data_importers.event_types import DataEventType
from data_importers.models import DataEvent
from django.test import TestCase


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
