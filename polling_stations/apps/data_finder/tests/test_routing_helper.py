from collections import namedtuple

from councils.tests.factories import CouncilFactory
from data_finder.helpers import RoutingHelper
from django.core.management import call_command
from django.test import TestCase

MockAddress = namedtuple(
    "MockAddress",
    ["address", "postcode", "council", "uprn", "polling_station_id", "location"],
)


class RoutingHelperTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="X01",
            identifiers=["X01"],
            geography__geography=None,
        )

        for fixture in [
            "test_single_address_single_polling_station.json",
            "test_single_address_blank_polling_station.json",
            "test_multiple_addresses_single_polling_station.json",
            "test_multiple_polling_stations.json",
            "test_multiple_polling_stations_with_null",
        ]:
            call_command(  # Hack to avoid converting all fixtures to factories
                "loaddata",
                fixture,
                verbosity=0,
            )

    def setUp(self):
        self.no_addresses_rh = RoutingHelper("")
        self.zero_stations_rh = RoutingHelper("")
        self.zero_stations_rh.addresses = [
            MockAddress(
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
            MockAddress(
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
            MockAddress(
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
        # for data in [("1", "0"), ("2", "1"), ("3", "2"), ("4", "2"), ("5","")]:
        #     Address.objects.update_or_create(pk = data[0])
        #
        rh.addresses = [
            MockAddress(
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
