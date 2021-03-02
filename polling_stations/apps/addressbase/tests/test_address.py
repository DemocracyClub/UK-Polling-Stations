from django.test import TestCase

from addressbase.models import UprnToCouncil
from addressbase.tests.factories import UprnToCouncilFactory
from councils.tests.factories import CouncilFactory


class TestAddressFactory(TestCase):
    def test_get_council_from_others_in_postcode(self):
        council_abc = CouncilFactory(pk="ABC", identifiers=["X01000000"])
        UprnToCouncilFactory.create_batch(3, lad="X01000000", uprn__postcode="AA11AA")

        uprns = UprnToCouncil.objects.all()
        uprn = uprns[0]
        address = uprn.uprn
        uprn.delete()
        self.assertEqual(address.get_council_from_others_in_postcode(), council_abc)

    def test_get_council_from_others_in_postcode_ambiguous(self):
        CouncilFactory(pk="ABC", identifiers=["X01000000"])
        UprnToCouncilFactory.create_batch(2, lad="X01000000", uprn__postcode="AA11AA")
        UprnToCouncilFactory.create_batch(2, lad="X01000002", uprn__postcode="AA11AA")
        uprns = UprnToCouncil.objects.filter(lad="X01000000")
        uprn = uprns[0]
        address = uprn.uprn
        uprn.delete()
        self.assertIsNone(address.get_council_from_others_in_postcode())
