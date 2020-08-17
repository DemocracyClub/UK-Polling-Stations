from collections import namedtuple
from django.test import TestCase

from councils.models import Council
from data_collection.tests.stubs import stub_halaroseimport
from pollingstations.models import PollingStation, ResidentialAddress


class HalaroseImportTests(TestCase):

    opts = {"noclean": False, "nochecks": True, "verbosity": 0}

    def setUp(self):
        Council.objects.update_or_create(pk="X01000000", identifiers=["X01000000"])
        cmd = stub_halaroseimport.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        addresses = (
            ResidentialAddress.objects.filter(council_id="X01000000")
            .order_by("address")
            .values_list("address", flat=True)
        )

        # we should have inserted 3 addresses
        # and discarded 3 due to error conditions
        self.assertEqual(3, len(addresses))
        expected = set(
            [
                "1 Heol Elfed, Gorseinon, Swansea",
                "47 Heol Dylan, Gorseinon, Swansea",
                "2, Dogkennel Farm Cottages",
            ]
        )
        self.assertEqual(set(addresses), expected)

    def test_station_ids(self):
        self.assertEqual(
            "",
            ResidentialAddress.objects.get(
                slug="x01000000-2-dogkennel-farm-cottages-ba152bb"
            ).polling_station_id,
        )
        self.assertEqual(
            "10-penyrheol-boxing-club",
            ResidentialAddress.objects.get(
                slug="x01000000-10-penyrheol-boxing-club-1-heol-elfed-gorseinon-swansea-sa44gh"
            ).polling_station_id,
        )
        self.assertEqual(
            "10-penyrheol-boxing-club",
            ResidentialAddress.objects.get(
                slug="x01000000-10-penyrheol-boxing-club-47-heol-dylan-gorseinon-swansea-sa44lr"
            ).polling_station_id,
        )

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="X01000000")
            .order_by("internal_council_id")
            .values_list("address", flat=True)
        )

        # we inserted 2 stations, even though only one of them
        # had no valid addresses associated with it
        self.assertEqual(2, len(stations))
        expected = set(
            [
                "Penyrheol Boxing Club\nGower View Road\nPenyrheol\nSwansea",
                "St Ambrose Church Hall\nWest Cliff Road\nBournemouth",
            ]
        )
        self.assertEqual(set(stations), expected)

    def test_address_formatter(self):
        HalaroseAddress = namedtuple(
            "HalaroseAddress",
            [
                "housename",
                "housenumber",
                "substreetname",
                "streetnumber",
                "streetname",
                "locality",
                "town",
                "adminarea",
            ],
        )

        test_cases = [
            {
                "in": HalaroseAddress(
                    housename="Mill Cottage",
                    housenumber="",
                    substreetname="",
                    streetnumber="",
                    streetname="Parkside",
                    locality="",
                    town="Cleator Moor",
                    adminarea="Cumbria",
                ),
                "out": "Mill Cottage, Parkside, Cleator Moor, Cumbria",
            },
            {
                "in": HalaroseAddress(
                    housename="The Elders",
                    housenumber="6",
                    substreetname="",
                    streetnumber="",
                    streetname="Church Street",
                    locality="",
                    town="Frizington",
                    adminarea="Cumbria",
                ),
                "out": "The Elders, 6 Church Street, Frizington, Cumbria",
            },
            {
                "in": HalaroseAddress(
                    housename="",
                    housenumber="1",
                    substreetname="The Croft",
                    streetnumber="",
                    streetname="Wilton",
                    locality="",
                    town="Egremont",
                    adminarea="Cumbria",
                ),
                "out": "1 The Croft, Wilton, Egremont, Cumbria",
            },
            {
                "in": HalaroseAddress(
                    housename="Flat 1",
                    housenumber="",
                    substreetname="Wulstan Hall",
                    streetnumber="139",
                    streetname="Queen Street",
                    locality="",
                    town="Whitehaven",
                    adminarea="Cumbria",
                ),
                "out": "Flat 1, Wulstan Hall, 139 Queen Street, Whitehaven, Cumbria",
            },
            {
                "in": HalaroseAddress(
                    housename="The Cottage",
                    housenumber="",
                    substreetname="Laurel Court",
                    streetnumber="",
                    streetname="Rheda Park",
                    locality="",
                    town="Frizington",
                    adminarea="Cumbria",
                ),
                "out": "The Cottage, Laurel Court, Rheda Park, Frizington, Cumbria",
            },
            {
                "in": HalaroseAddress(
                    housename="",
                    housenumber="3B",
                    substreetname="CLIVE COURT",
                    streetnumber="24",
                    streetname="GRAND PARADE",
                    locality="",
                    town="EASTBOURNE",
                    adminarea="EAST SUSSEX",
                ),
                "out": "3B CLIVE COURT, 24 GRAND PARADE, EASTBOURNE, EAST SUSSEX",
            },
        ]
        cmd = stub_halaroseimport.Command()
        for case in test_cases:
            self.assertEqual(case["out"], cmd.get_residential_address(case["in"]))
