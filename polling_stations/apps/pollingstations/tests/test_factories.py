from councils.models import Council
from django.test import TestCase
from pollingstations.tests.factories import (
    AdvanceVotingStationFactory,
    PollingDistrictFactory,
    PollingStationFactory,
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


class TestAdvanceVotingStationFactory(TestCase):
    def test_advance_voting_station_factory(self):
        advance_station = AdvanceVotingStationFactory(
            postcode="CF99 1SN", name="Welsh Parliament"
        )
        self.assertEqual(str(advance_station), "Welsh Parliament (CF99 1SN)")
