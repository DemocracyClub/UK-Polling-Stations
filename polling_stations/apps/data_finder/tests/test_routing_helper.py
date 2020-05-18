from unittest import mock

from django.http import QueryDict
from django.test import TestCase
from addressbase.models import UprnInfo
from data_finder.helpers import RoutingHelper


class RoutingHelperTest(TestCase):
    fixtures = [
        "test_single_address_single_polling_station.json",
        "test_single_address_blank_polling_station.json",
        "test_multiple_addresses_single_polling_station.json",
        "test_multiple_polling_stations.json",
        "test_multiple_polling_stations_with_null",
    ]

    def setUp(self):
        self.no_addresses_rh = RoutingHelper("")
        self.zero_stations_rh = RoutingHelper("")
        self.zero_stations_rh.addresses = [
            UprnInfo(
                address="",
                postcode="",
                council="",
                uprn="",
                polling_station_id="",
                location="",
            )
            for _ in range(3)
        ]
        self.one_station_rh = RoutingHelper("")
        self.one_station_rh.addresses = [
            UprnInfo(
                address="",
                postcode="",
                council="",
                uprn="",
                polling_station_id="1A",
                location="",
            )
            for _ in range(3)
        ]
        self.three_stations_rh = RoutingHelper("")
        self.three_stations_rh.addresses = [
            UprnInfo(
                address="",
                postcode="",
                council="",
                uprn="",
                polling_station_id=f"{x}A",
                location="",
            )
            for x in range(3)
        ]

    def test_has_addresses(self):
        self.assertFalse(self.no_addresses_rh.has_addresses)
        for rh in [self.zero_stations_rh, self.one_station_rh, self.three_stations_rh]:
            self.assertTrue(rh.has_addresses)

    def test_no_stations(self):
        self.assertTrue(self.zero_stations_rh.no_stations)
        for rh in [self.no_addresses_rh, self.one_station_rh, self.three_stations_rh]:
            self.assertFalse(rh.no_stations)

    def test_addresses_have_single_station(self):
        self.assertTrue(self.one_station_rh.addresses_have_single_station)
        self.assertFalse(self.no_addresses_rh.addresses_have_single_station)
        self.assertFalse(self.zero_stations_rh.addresses_have_single_station)
        self.assertFalse(self.three_stations_rh.addresses_have_single_station)

    def test_polling_stations(self):
        rh = RoutingHelper("")
        rh.addresses = [
            UprnInfo(
                address="",
                postcode="",
                council="",
                uprn="",
                polling_station_id=x,
                location="",
            )
            for x in ["0", "1", "2", "2", ""]
        ]  # Count duplicate polling stations once & Make sure we include the "blank" polling stations
        self.assertEqual(len(rh.addresses), 5)
        self.assertEqual({"0", "1", "2", ""}, rh.polling_stations)

    def test_single_address_single_polling_station(self):
        postcode_base = "AA1 1AA"
        postcodes = [
            postcode_base,
            postcode_base.lower(),
            postcode_base.replace(" ", ""),
            postcode_base.replace(" ", "").lower(),
        ]
        for postcode in postcodes:
            rh = RoutingHelper(postcode)
            self.assertEqual("address_view", rh.view)

    def test_single_address_blank_polling_station(self):
        # Test fixtures include a polling station,
        # but only address has blank station_id
        rh = RoutingHelper("BB1 1BB")
        self.assertEqual("postcode_view", rh.view)

    def test_multiple_addresses_single_polling_station(self):
        rh = RoutingHelper("CC1 1AA")
        self.assertEqual("address_view", rh.view)

    def test_multiple_polling_stations(self):
        rh = RoutingHelper("DD1 1DD")
        self.assertEqual("address_select_view", rh.view)

    def test_multiple_polling_stations_with_null(self):
        rh = RoutingHelper("EE1 1EE")
        self.assertEqual("address_select_view", rh.view)

    def test_canonical_url(self):
        rh = RoutingHelper("CC11AA")
        request = mock.Mock()
        request.GET = QueryDict("utm_source=foo&something=other")
        # Could be either uprn
        self.assertRegex(
            rh.get_canonical_url(request), r"/address/10[23]/\?utm_source=foo"
        )

    def test_canonical_url_without_preserve(self):
        rh = RoutingHelper("CC11AA")
        request = mock.Mock()
        request.GET = QueryDict("utm_source=foo&something=other")
        # Could be either uprn
        self.assertRegex(
            rh.get_canonical_url(request, preserve_query=False), r"/address/10[23]/"
        )
