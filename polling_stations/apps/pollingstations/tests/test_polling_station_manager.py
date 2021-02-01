from django.core.management import call_command
from django.test import TestCase

from councils.tests.factories import CouncilFactory
from pollingstations.models import PollingStation


class PollingStationsStationIdTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="ABC",
            name="ABC council",
            identifiers=["X01000001"],
            geography__geography=None,
        )
        CouncilFactory(
            council_id="DEF",
            name="DEF council",
            identifiers=["X01000002"],
            geography__geography=None,
        )

        call_command(  # Hack to avoid converting all fixtures to factories
            "loaddata",
            "polling_stations/apps/pollingstations/fixtures/test_polling_stations_station_id.json",
            verbosity=0,
        )

    def test_formatted_address(self):
        station = PollingStation.objects.get(pk=1)
        self.assertEqual(station.formatted_address, "St Foo's Church Hall\nBar Town")

    def test_str(self):
        station1 = PollingStation.objects.get(pk=1)
        station2 = PollingStation.objects.get(pk=3)
        self.assertEqual(str(station1), "1 (ABC council)")
        self.assertEqual(str(station2), "1 (DEF council)")
