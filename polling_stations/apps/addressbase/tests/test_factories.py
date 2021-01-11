from django.test import TestCase

from addressbase.models import Address
from addressbase.tests.factories import AddressFactory, UprnToCouncilFactory


class TestAddressFactory(TestCase):
    def test_address_factory(self):
        address = AddressFactory()
        self.assertEqual(len(address.uprn), 9)
        self.assertEqual(address.addressbase_postal, "D")


class TestUprnToCouncilFactory(TestCase):
    def test_uprn_to_council_factory(self):
        uprn_to_council = UprnToCouncilFactory()
        self.assertIsInstance(uprn_to_council.uprn, Address)
