from django.test import TestCase

from addressbase.models import UprnToCouncil, Address
from councils.models import Council
from data_importers.tests.stubs import stub_dcountsimport
from pollingstations.models import PollingStation


class DemocracyCountsImportTests(TestCase):

    opts = {"nochecks": True, "verbosity": 0}
    uprns = ["1", "2", "3", "4", "5", "6"]
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

        Council.objects.update_or_create(pk="AAA", identifiers=["X01000000"])
        for uprn in self.uprns:
            UprnToCouncil.objects.update_or_create(pk=uprn, lad="AAA")
        cmd = stub_dcountsimport.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        imported_uprns = (
            UprnToCouncil.objects.filter(lad="AAA")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", flat=True)
        )

        # we should have inserted 4 addresses
        # and discarded 2 due to error conditions
        self.assertEqual(4, len(imported_uprns))
        expected = set(
            [
                "1",
                "3",
                "5",
                "6",
            ]
        )
        self.assertEqual(set(imported_uprns), expected)

    def test_station_ids(self):
        imported_uprns_and_ids = (
            UprnToCouncil.objects.filter(lad="AAA")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )

        expected = set(
            [
                ("1", "B6/1"),
                ("3", "B6/1"),
                ("5", "B60/1"),
                ("6", "B60/1"),
            ]
        )
        self.assertEqual(set(imported_uprns_and_ids), expected)

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="AAA")
            .order_by("internal_council_id")
            .values_list("address", flat=True)
        )

        self.assertEqual(2, len(stations))
        expected = set(
            [
                "Q.E. Boys School\nQueens Road\nBarnet\nHerts",
                "Our Lady of Lourdes RC Primary School\nBow Lane\nFinchley\nLondon",
            ]
        )
        self.assertEqual(set(stations), expected)
