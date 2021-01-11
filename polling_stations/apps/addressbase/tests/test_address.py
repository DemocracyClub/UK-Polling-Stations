import factory
from django.test import TestCase

from addressbase.models import Address
from addressbase.tests.factories import UprnToCouncilFactory, AddressFactory
from councils.tests.factories import CouncilFactory
from pollingstations.tests.factories import PollingStationFactory


class AddressTest(TestCase):
    def setUp(self):
        self.council = CouncilFactory(council_id="AAA")
        self.uprn_without_station = UprnToCouncilFactory(
            uprn=factory.SubFactory(AddressFactory), lad=self.council.council_id
        )
        self.station = PollingStationFactory(council=self.council)
        self.uprn_with_station = UprnToCouncilFactory(
            uprn=factory.SubFactory(AddressFactory),
            lad=self.council.council_id,
            polling_station_id=self.station.internal_council_id,
        )
        self.address_no_station = Address.objects.get(
            pk=self.uprn_without_station.uprn.uprn
        )
        self.address_with_station = Address.objects.get(
            pk=self.uprn_with_station.uprn.uprn
        )
        self.addresses = [self.address_no_station, self.address_with_station]

    def test_council(self):
        for address in self.addresses:
            self.assertEqual(address.council, self.council)

    def test_council_id(self):
        for address in self.addresses:
            self.assertEqual(address.council, self.council)

    def test_polling_station(self):
        self.assertIsNone(self.address_no_station.polling_station)
        self.assertEqual(self.address_with_station.polling_station, self.station)

    def test_polling_station_id(self):
        self.assertEqual(self.address_no_station.polling_station_id, "")
        self.assertEqual(
            self.address_with_station.polling_station_id,
            self.station.internal_council_id,
        )
