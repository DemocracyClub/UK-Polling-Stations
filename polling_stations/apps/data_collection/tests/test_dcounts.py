from django.test import TestCase

from councils.models import Council
from data_collection.tests.stubs import stub_dcountsimport
from pollingstations.models import PollingStation, ResidentialAddress


class DemocracyCountsImportTests(TestCase):

    opts = {"noclean": False, "nochecks": True, "verbosity": 0}

    def setUp(self):
        Council.objects.update_or_create(pk="X01000000")
        cmd = stub_dcountsimport.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        addresses = (
            ResidentialAddress.objects.filter(council_id="X01000000")
            .order_by("address")
            .values_list("address", flat=True)
        )

        # we should have inserted 4 addresses
        # and discarded 2 due to error conditions
        self.assertEqual(4, len(addresses))
        expected = set(
            [
                "Flat 1, 196 Ballards Lane, Finchley, London",
                "Flat 3, 196 Ballards Lane, Finchley, London",
                "158 Wood Street, Barnet",
                "164 Wood Street, Barnet",
            ]
        )
        self.assertEqual(set(addresses), expected)

    def test_station_ids(self):
        self.assertEqual(
            "B6/1",
            ResidentialAddress.objects.get(
                slug="x01000000-b6-1-158-wood-street-barnet-en54db"
            ).polling_station_id,
        )
        self.assertEqual(
            "B6/1",
            ResidentialAddress.objects.get(
                slug="x01000000-b6-1-164-wood-street-barnet-en54db"
            ).polling_station_id,
        )
        self.assertEqual(
            "B60/1",
            ResidentialAddress.objects.get(
                slug="x01000000-b60-1-flat-1-196-ballards-lane-finchley-london-n32na"
            ).polling_station_id,
        )
        self.assertEqual(
            "B60/1",
            ResidentialAddress.objects.get(
                slug="x01000000-b60-1-flat-3-196-ballards-lane-finchley-london-n32na"
            ).polling_station_id,
        )

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="X01000000")
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
