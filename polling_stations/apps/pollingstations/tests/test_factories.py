from django.test import TestCase

from councils.models import Council
from pollingstations.tests.factories import (
    PollingStationFactory,
    PollingDistrictFactory,
)


class TestPollingStationFactory(TestCase):
    def test_polling_station_factory(self):
        station = PollingStationFactory()
        self.assertIsInstance(station.council, Council)
        self.assertRegex(station.internal_council_id, r"^PS-\d+$")


class TestPollingDistrictFactory(TestCase):
    def test_polling_district_factory(self):
        station = PollingDistrictFactory()
        self.assertIsInstance(station.council, Council)
        self.assertRegex(station.internal_council_id, r"^PD-\d+$")
