"""
Test that we're not serving wrong polling stations in the case where:

1. We only have shape data for districts
2. A given postcode doesn't fall within that district

This test sets up the following data (made up from locations at Kentwell Hall):

Districts:

    Little Melford: pk=117
    Barns Sward: pk=118
    Tourney Field: pk=119

Addresses:

    Tourney Field: pk=9999991
    The Cott: pk=9999992
    Sym's Caravan: pk=9999993

Polling Stations

    Tourney Field's: pk=117
    Barns Sward's: pk=118
    Little Melford: pk=119

With the initial set up, the postcode 'KW15 88TF' has two addresses, one falls
inside the 'Tourney Field' and the other is on the 'Barns Sward'.

We want to route someone living at the 'Tourney Field' address to the
'Tourney Field' polling station, and someone living at 'The Cott' to the Barns
Sward polling station.

To do this, we need to create ResidentialAddress objects for them.
"""

from operator import attrgetter

from django.test import TestCase

from addressbase.models import Address
from addressbase.helpers import (
    postcodes_not_contained_by_district,
    district_contains_all_points,
    EdgeCaseFixer,
    create_address_records_for_council,
)
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress
from councils.models import Council
from data_finder.helpers import RoutingHelper


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class PostcodeBoundaryFixerTestCase(TestCase):
    fixtures = ["test_kentwell_data.json"]

    def test_data_imported(self):
        def _check_ids_expected(id1, id2):
            BS_district = PollingDistrict.objects.get(pk=id1)
            BS_station = PollingStation.objects.get_polling_station_by_id(
                BS_district.polling_station_id, BS_district.council.pk
            )

            self.assertEqual(BS_station.pk, id2)

        expected_ids = ((117, 117), (118, 118), (119, 119))

        for id1, id2 in expected_ids:
            _check_ids_expected(id1, id2)

    def test_postcodes_for_district(self):
        district = PollingDistrict.objects.get(pk=117)
        postcodes = Address.objects.postcodes_for_district(district)
        self.assertEqual(postcodes, ["KW15 88LM"])

    def test_points_for_postcode(self):
        points = Address.objects.points_for_postcode("KW15 88LM")
        self.assertEqual(len(points), 1)
        self.assertAlmostEqual(points[0].x, 0.715235268482966)
        self.assertAlmostEqual(points[0].y, 52.095491167556695)

        points = Address.objects.points_for_postcode("KW15 88TF")
        self.assertEqual(len(points), 2)
        self.assertAlmostEqual(points[0].x, 0.7225083308451804)
        self.assertAlmostEqual(points[0].y, 52.09750519940858)

    def test_district_contains_all_points(self):
        district = PollingDistrict.objects.get(pk=117)
        points = Address.objects.points_for_postcode("KW15 88LM")
        self.assertTrue(district_contains_all_points(district, points))

        district = PollingDistrict.objects.get(pk=118)
        points = Address.objects.points_for_postcode("KW15 88TF")
        self.assertFalse(district_contains_all_points(district, points))

    def test_postcodes_not_contained_by_district(self):
        district = PollingDistrict.objects.get(pk=117)
        postcodes = postcodes_not_contained_by_district(district)
        self.assertEqual(postcodes["not_contained"], [])
        self.assertEqual(postcodes["total"], 1)

        district = PollingDistrict.objects.get(pk=118)
        postcodes = postcodes_not_contained_by_district(district)
        self.assertEqual(postcodes["not_contained"], ["KW15 88TF"])
        self.assertEqual(postcodes["total"], 1)

    def test_create_address_records_for_council(self):
        council = Council.objects.get(pk="X01000001")
        postcode_report = create_address_records_for_council(
            council, 1000, MockLogger()
        )

        self.assertEqual(postcode_report["no_attention_needed"], 1)
        self.assertTrue(
            "KW15 88TF" in postcode_report["postcodes_needing_address_lookup"]
        )
        self.assertFalse(
            "KW15 88LM" in postcode_report["postcodes_needing_address_lookup"]
        )

    def test_make_addresses_for_postcode(self):
        # Before the fix, we wrongly assume that we know the polling station
        postcode = "KW15 88TF"
        rh = RoutingHelper(postcode)
        endpoint = rh.get_endpoint()
        self.assertEqual("postcode_view", endpoint.view)

        # Fix the addresses outside of the districts
        fixer = EdgeCaseFixer("X01000001", MockLogger())
        fixer.make_addresses_for_postcode(postcode)
        fixer.get_address_set().save(1000)

        # Now we should get offered an address lookup
        rh = RoutingHelper(postcode)
        endpoint = rh.get_endpoint()
        self.assertEqual("address_select_view", endpoint.view)

    def test_make_addresses_cross_borders(self):
        """
        Ensure that we make addresses for both sides of a district.

        We should see 2 ResidentialAddress after calling
        make_addresses_for_postcode.
        """

        # We don't have any addresses yet
        self.assertEqual(ResidentialAddress.objects.all().count(), 0)

        # Fix the addresses outside of the districts
        postcode = "KW15 88TF"
        fixer = EdgeCaseFixer("X01000001", MockLogger())
        fixer.make_addresses_for_postcode(postcode)
        fixer.get_address_set().save(1000)

        self.assertEqual(ResidentialAddress.objects.all().count(), 2)

    def test_addresses_cross_borders_with_orphan_distirct(self):
        """
        In this case, we have a postcode which contains addresses in one
        district where we do know the polling station and one where we don't
        We should still insert addresses for both districts
        """
        postcode = "KW15 88LX"
        fixer = EdgeCaseFixer("X01000001", MockLogger())
        fixer.make_addresses_for_postcode(postcode)
        addresses = fixer.get_address_set()
        records = sorted(list(addresses), key=attrgetter("address"))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].address, "74 Kendell Street")
        self.assertEqual(records[0].polling_station_id, "1")
        # this address falls in the invalid district
        self.assertEqual(records[1].address, "75 Kendell Street")
        self.assertEqual(records[1].polling_station_id, "")

    def test_addresses_cross_borders_with_overlapping_distirct(self):
        """
        In this case, we have a postcode which contains an addresses in
        an overlap between 2 districts (both of which we know a station for).
        We should still insert addresses for all addresses
        even though we can't map all of them to a poling station
        """
        postcode = "KW15 88LZ"
        fixer = EdgeCaseFixer("X01000001", MockLogger())
        fixer.make_addresses_for_postcode(postcode)
        addresses = fixer.get_address_set()
        records = sorted(list(addresses), key=attrgetter("address"))
        self.assertEqual(len(records), 3)
        # 80 Kendell Street is wholly in one district
        self.assertEqual(records[0].address, "80 Kendell Street")
        self.assertEqual(records[0].polling_station_id, "1")
        # 81 Kendell Street is in the overlap
        self.assertEqual(records[1].address, "81 Kendell Street")
        self.assertEqual(records[1].polling_station_id, "")
        # 82 Kendell Street is wholly in one district
        self.assertEqual(records[2].address, "82 Kendell Street")
        self.assertEqual(records[2].polling_station_id, "2")
