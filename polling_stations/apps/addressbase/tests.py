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

from django.test import TestCase

from addressbase.models import Address
from addressbase.helpers import (postcodes_not_contained_by_district,
                                 district_contains_all_points,
                                 make_addresses_for_postcode,
                                 districts_requiring_address_lookup)
from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council
from data_finder.helpers import RoutingHelper


class PostcodeBoundaryFixerTestCase(TestCase):
    fixtures = ['test_kentwell_data.json']

    def test_data_imported(self):

        def _check_ids_expected(id1, id2):
            BS_district = PollingDistrict.objects.get(pk=id1)
            BS_station = PollingStation.objects.get_polling_station_by_id(
                BS_district.polling_station_id,
                BS_district.council.pk
            )

            self.assertEqual(BS_station.pk, id2)

        expected_ids = (
            (117, 117),
            (118, 118),
            (119, 119),
        )

        for id1, id2 in expected_ids:
            _check_ids_expected(id1, id2)

    def test_postcodes_for_district(self):
        district = PollingDistrict.objects.get(pk=117)
        postcodes = Address.objects.postcodes_for_district(district)
        self.assertEqual(postcodes, ['KW15 88LM'])

    def test_points_for_postcode(self):
        points = Address.objects.points_for_postcode('KW15 88LM')
        self.assertEqual(len(points), 1)
        self.assertAlmostEqual(points[0].x, 0.715235268482966)
        self.assertAlmostEqual(points[0].y, 52.095491167556695)

        points = Address.objects.points_for_postcode('KW15 88TF')
        self.assertEqual(len(points), 2)
        self.assertAlmostEqual(points[0].x, 0.7225083308451804)
        self.assertAlmostEqual(points[0].y, 52.09750519940858)

    def test_district_contains_all_points(self):
        district = PollingDistrict.objects.get(pk=117)
        points = Address.objects.points_for_postcode('KW15 88LM')
        self.assertTrue(district_contains_all_points(district, points))

        district = PollingDistrict.objects.get(pk=118)
        points = Address.objects.points_for_postcode('KW15 88TF')
        self.assertFalse(district_contains_all_points(district, points))

    def test_postcodes_not_contained_by_district(self):
        district = PollingDistrict.objects.get(pk=117)
        postcodes = postcodes_not_contained_by_district(district)
        self.assertEqual(postcodes['not_contained'], [])
        self.assertEqual(postcodes['total'], 1)

        district = PollingDistrict.objects.get(pk=118)
        postcodes = postcodes_not_contained_by_district(district)
        self.assertEqual(postcodes['not_contained'], ['KW15 88TF'])
        self.assertEqual(postcodes['total'], 1)

    def test_districts_requiring_address_lookup(self):
        council = Council.objects.get(pk='X01000001')
        postcode_report = districts_requiring_address_lookup(council)

        self.assertEqual(postcode_report['no_attention_needed'], 1)
        self.assertTrue(
            ['KW15 88TF'] in postcode_report['address_lookup_needed'].values())
        self.assertFalse(
            ['KW15 88LM'] in postcode_report['address_lookup_needed'].values())


    def test_make_addresses_for_postcode(self):
        # Before the fix, we wrongly assume that we know the polling station
        postcode = 'KW15 88TF'
        rh = RoutingHelper(postcode)
        endpoint = rh.get_endpoint()
        self.assertEqual('postcode_view', endpoint.view)

        # Fix the addresses outside of the districts
        make_addresses_for_postcode(postcode)

        # Now we should get offered an address lookup
        rh = RoutingHelper(postcode)
        endpoint = rh.get_endpoint()
        self.assertEqual('address_select_view', endpoint.view)
