from collections import namedtuple

from addressbase.models import Address, UprnToCouncil
from councils.tests.factories import CouncilFactory
from data_importers.tests.stubs import stub_halaroseimport, stub_halarose2026import
from django.test import TestCase
from pollingstations.models import PollingStation


class HalaroseImportTests(TestCase):
    opts = {"nochecks": True, "verbosity": 0, "include_past_elections": True}
    uprns = [
        "1",
        "2",
        "3",
        "4",
    ]
    addressbase = [
        {
            "address": "2, Dogkennel Farm Cottages",
            "postcode": "BA15 2BB",
            "uprn": "1",
        },
        {
            "address": "47 Heol Dylan, Gorseinon, Swansea",
            "postcode": "SA4 4LR",
            "uprn": "2",
        },
        {
            "address": "1 Heol Elfed, Gorseinon, Swansea",
            "postcode": "SA4 4GH",
            "uprn": "3",
        },
        {
            "address": "2 Heol Elfed, Gorseinon, Swansea",
            "postcode": "SA4 4GH",
            "uprn": "4",
        },
    ]

    def setUp(self):
        for address in self.addressbase:
            Address.objects.update_or_create(**address)

        CouncilFactory(pk="AAA", identifiers=["X01000000"])
        for uprn in self.uprns:
            UprnToCouncil.objects.update_or_create(pk=uprn, lad="X01000000")
        cmd = stub_halaroseimport.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", flat=True)
        )

        self.assertEqual(2, len(imported_uprns))
        expected = {"2", "3"}
        self.assertEqual(set(imported_uprns), expected)

    def test_station_ids(self):
        imported_uprns_and_ids = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )

        expected = {
            ("2", "10-penyrheol-boxing-club"),
            ("3", "10-penyrheol-boxing-club"),
        }
        self.assertEqual(set(imported_uprns_and_ids), expected)

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="AAA")
            .order_by("internal_council_id")
            .values_list("address", flat=True)
        )

        # we inserted 2 stations, even though only one of them
        # had no valid addresses associated with it
        self.assertEqual(2, len(stations))
        expected = {
            "Penyrheol Boxing Club\nGower View Road\nPenyrheol\nSwansea",
            "St Ambrose Church Hall\nWest Cliff Road\nBournemouth",
        }
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


class Halarose2026ImportTests(TestCase):
    opts = {"nochecks": True, "verbosity": 0, "include_past_elections": True}
    uprns = [
        "1",
        "2",
        "3",
        "4",
        "5",
    ]
    addressbase = [
        {
            "address": "1 Parsonage Fold, Beetham, Milnthorpe, Cumbria",
            "postcode": "LA7 7RJ",
            "uprn": "1",
        },
        {
            "address": "18 Hillcrest Drive, Slackhead, Milnthorpe, Cumbria",
            "postcode": "LA7 7BB",
            "uprn": "2",
        },
        {
            "address": "Low Barn, Whassett, Milnthorpe, Cumbria",
            "postcode": "LA7 7DN",
            "uprn": "3",
        },
        {
            "address": "Honeysuckle Cottage 2 Parsonage Fold, Beetham, Milnthorpe, Cumbria",
            "postcode": "LA7 7RJ",
            "uprn": "4",
        },
        {
            "address": "1 Ash Court	Ackenthwaite, Milnthorpe, Cumbria",
            "postcode": "LA7 7GL",
            "uprn": "5",
        },
    ]

    def setUp(self):
        for address in self.addressbase:
            Address.objects.update_or_create(**address)

        CouncilFactory(pk="AAA", identifiers=["X01000000"])
        for uprn in self.uprns:
            UprnToCouncil.objects.update_or_create(pk=uprn, lad="X01000000")
        cmd = stub_halarose2026import.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", flat=True)
        )

        self.assertEqual(3, len(imported_uprns))
        expected = {"1", "2", "3"}
        self.assertEqual(set(imported_uprns), expected)

    def test_station_ids(self):
        imported_uprns_and_ids = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )

        expected = {
            ("1", "3-the-heron-theatre"),
            ("2", "4-the-heron-theatre"),
            ("3", "4-the-heron-theatre"),
        }
        self.assertEqual(set(imported_uprns_and_ids), expected)

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="AAA")
            .order_by("internal_council_id")
            .values_list("address", flat=True)
        )

        self.assertEqual(3, len(stations))
        expected = {
            "The Heron Theatre\nBeetham",  # there are two stations at this venue
            "Parish Hall\nChrist the King RC Church\nHaverflatts Lane\nMilnthorpe",
        }
        self.assertEqual(set(stations), expected)
