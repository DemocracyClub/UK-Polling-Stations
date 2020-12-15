from django.test import TestCase
from pollingstations.models import PollingStation


class PollingStationsStationIdTest(TestCase):
    fixtures = ["test_polling_stations_station_id.json"]

    def test_formatted_address(self):
        station = PollingStation.objects.get(pk=1)
        self.assertEqual(station.formatted_address, "St Foo's Church Hall\nBar Town")

    def test_str(self):
        station1 = PollingStation.objects.get(pk=1)
        station2 = PollingStation.objects.get(pk=3)
        self.assertEqual(str(station1), "1 (ABC council)")
        self.assertEqual(str(station2), "1 (DEF council)")
