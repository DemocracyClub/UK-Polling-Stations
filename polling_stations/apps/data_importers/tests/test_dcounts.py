from addressbase.models import Address, UprnToCouncil
from councils.tests.factories import CouncilFactory
from data_importers.tests.stubs import stub_dcountsimport
from django.test import TestCase
from pollingstations.models import PollingStation


class DemocracyCountsImportTests(TestCase):
    opts = {"nochecks": True, "verbosity": 0, "include_past_elections": True}
    uprns = ["1", "2", "3", "5", "6"]
    addressbase = [
        {
            "address": "158 Wood Street,Barnet",
            "postcode": "EN5 4DB",
            "uprn": "1",
        },
        {
            "address": "162 Wood Street,Barnet",
            "postcode": "EN5 4DB",
            "uprn": "2",
        },
        {
            "address": "164 Wood Street,Barnet",
            "postcode": "EN5 4DB",
            "uprn": "3",
        },
        # uprn '4' in districts.csv but wasn't in addressbase
        {
            "address": "Flat 1,196 Ballards Lane,Finchley,London",
            "postcode": "N3 2NA",
            "uprn": "5",
        },
        {
            "address": "Flat 3,196 Ballards Lane,Finchley,London",
            "postcode": "N3 2NA",
            "uprn": "6",
        },
    ]

    def setUp(self):
        for address in self.addressbase:
            Address.objects.update_or_create(**address)

        CouncilFactory(pk="AAA", identifiers=["X01000000"])
        for uprn in self.uprns:
            UprnToCouncil.objects.update_or_create(pk=uprn, lad="X01000000")
        cmd = stub_dcountsimport.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", flat=True)
        )

        # we should have inserted 4 addresses
        # and discarded 2 due to error conditions
        self.assertEqual(4, len(imported_uprns))
        expected = {
            "1",
            "3",
            "5",
            "6",
        }
        self.assertEqual(set(imported_uprns), expected)

    def test_station_ids(self):
        imported_uprns_and_ids = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )

        expected = {
            ("1", "B6/1"),
            ("3", "B6/1"),
            ("5", "B60/1"),
            ("6", "B60/1"),
        }
        self.assertEqual(set(imported_uprns_and_ids), expected)

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="AAA")
            .order_by("internal_council_id")
            .values_list("address", flat=True)
        )

        self.assertEqual(2, len(stations))
        expected = {
            "Q.E. Boys School\nQueens Road\nBarnet\nHerts",
            "Our Lady of Lourdes RC Primary School\nBow Lane\nFinchley\nLondon",
        }
        self.assertEqual(set(stations), expected)
