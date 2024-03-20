from councils.models import Council
from django.db import IntegrityError, transaction
from django.test import TestCase
from pollingstations.models import PollingStation
from pollingstations.tests.factories import (
    AccessibilityInformationFactory,
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


class TestAccessibilityInformationFactory(TestCase):
    def test_accessibility_information_factory(self):
        AccessibilityInformationFactory()
        self.assertEqual(len(PollingStation.objects.all()), 1)

    def test_accessibility_information_factory_constraint(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            AccessibilityInformationFactory(level_access=True, temporary_ramp=True)

        AccessibilityInformationFactory(level_access=True, temporary_ramp=False)
        AccessibilityInformationFactory(level_access=False, temporary_ramp=True)
        AccessibilityInformationFactory(level_access=False, temporary_ramp=False)
        AccessibilityInformationFactory(level_access=None, temporary_ramp=True)
        AccessibilityInformationFactory(level_access=None, temporary_ramp=False)
