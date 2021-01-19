from django.test import TestCase
from uk_geo_utils.models import Onspd

from addressbase.models import UprnToCouncil, Address
from councils.models import Council
from data_finder.tests.utils import PostcodeBuilder


class TestPostcodeTestCase(TestCase):
    def test_construction(self):
        postcode = PostcodeBuilder()
        self.assertIsInstance(postcode.postcode, str)
        self.assertEqual(len(postcode.councils), 1)
        self.assertIsInstance(postcode.councils[0], Council)
        self.assertEqual(postcode.councils[0].council_id[0], "E")

    def test_construction_with_multiple_councils(self):
        postcode = PostcodeBuilder(multiple_councils=True, nations="W")
        self.assertEqual(len(postcode.councils), 2)
        self.assertEqual(
            set(council.council_id[0] for council in postcode.councils), {"W"}
        )

    def test_construction_with_multiple_nations(self):
        postcode = PostcodeBuilder(multiple_councils=True, nations=("E", "S"))
        self.assertEqual(len(postcode.councils), 2)
        self.assertEqual(postcode.councils[0].council_id[0], "E")
        self.assertEqual(postcode.councils[1].council_id[0], "S")

    def test_postcode_not_duplicated(self):
        postcode_1 = PostcodeBuilder()
        postcode_2 = PostcodeBuilder()
        self.assertNotEqual(postcode_1.postcode, postcode_2.postcode)

    def test_in_onspd(self):
        postcode = PostcodeBuilder().in_onspd()
        self.assertEqual(
            postcode.postcode, Onspd.objects.get(pcds=postcode.postcode).pcds
        )

    def test_with_addresses(self):
        postcode = PostcodeBuilder().with_unassigned_addresses()
        self.assertEqual(len(UprnToCouncil.objects.all()), 1)
        self.assertEqual(len(Address.objects.all()), 1)
        self.assertEqual(len(postcode.unassigned_addresses), 1)
        self.assertTrue(
            postcode.councils[0].area.contains(Address.objects.all()[0].location)
        )

    def test_with_addresses_multiple_councils(self):
        postcode = PostcodeBuilder(multiple_councils=True).with_unassigned_addresses()
        self.assertEqual(len(postcode.unassigned_addresses), 2)
        for council in postcode.councils:
            uprn = UprnToCouncil.objects.get(lad=council.council_id)
            self.assertTrue(council.area.contains(uprn.uprn.location))
            self.assertTrue(postcode.geometry.contains(uprn.uprn.location))

    def test_with_assigned_addresses(self):
        postcode = PostcodeBuilder().with_assigned_addresses()
        self.assertEqual(len(postcode.stations), 1)
        for address in postcode.addresses:
            self.assertEqual(
                UprnToCouncil.objects.get(uprn=address.uprn).polling_station_id,
                postcode.stations[0].internal_council_id,
            )
