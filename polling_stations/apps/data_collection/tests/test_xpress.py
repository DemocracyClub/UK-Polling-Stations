from django.test import TestCase

from councils.models import Council
from data_collection.tests.stubs import stub_xpress_democlub, stub_xpress_weblookup
from pollingstations.models import PollingStation, ResidentialAddress


class XpressDemocracyClubImportTests(TestCase):

    opts = {"noclean": False, "nochecks": True, "verbosity": 0}

    def setUp(self):
        Council.objects.update_or_create(pk="X01000000")
        cmd = stub_xpress_democlub.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        addresses = (
            ResidentialAddress.objects.filter(council_id="X01000000")
            .order_by("address")
            .values_list("address", flat=True)
        )

        # 4 records should have been inserted, and one discarded
        self.assertEqual(4, len(addresses))
        expected = set(
            [
                "1 Freshbrook Mews, Freshbrook Road, Lancing, West Sussex",
                "2 Freshbrook Mews, Freshbrook Road, Lancing, West Sussex",
                "1 Abbots Way, Lancing, West Sussex",
                "2 Abbots Way, Lancing, West Sussex",
            ]
        )
        self.assertEqual(set(addresses), expected)

    def test_station_ids(self):
        self.assertEqual(
            "518",
            ResidentialAddress.objects.get(
                slug="x01000000-518-1-abbots-way-lancing-west-sussex-bn159dh"
            ).polling_station_id,
        )
        self.assertEqual(
            "518",
            ResidentialAddress.objects.get(
                slug="x01000000-518-2-abbots-way-lancing-west-sussex-bn159dh"
            ).polling_station_id,
        )
        self.assertEqual(
            "512",
            ResidentialAddress.objects.get(
                slug="x01000000-512-1-freshbrook-mews-freshbrook-road-lancing-west-sussex-bn158da"
            ).polling_station_id,
        )
        self.assertEqual(
            "512",
            ResidentialAddress.objects.get(
                slug="x01000000-512-2-freshbrook-mews-freshbrook-road-lancing-west-sussex-bn158da"
            ).polling_station_id,
        )

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="X01000000")
            .order_by("internal_council_id")
            .values_list("address", flat=True)
        )

        # check we inserted 2 stations
        self.assertEqual(2, len(stations))
        expected = set(
            [
                "Lancing Parish Hall\nSouth Street\nLancing",
                "Monks Farm Hall\nNorth Road\nLancing",
            ]
        )
        self.assertEqual(set(stations), expected)


class XpressWebLookupImportTests(TestCase):

    opts = {"noclean": False, "nochecks": True, "verbosity": 0}

    def setUp(self):
        Council.objects.update_or_create(pk="X01000000")
        cmd = stub_xpress_weblookup.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        addresses = (
            ResidentialAddress.objects.filter(council_id="X01000000")
            .order_by("address")
            .values_list("address", flat=True)
        )

        # we should have inserted 4 addresses
        # discarded 1 due to error condition
        # and merged 2 together
        self.assertEqual(4, len(addresses))
        expected = set(
            [
                "Balham High Road",  # 2 records will have been merged into 1 here
                "189 Balham High Road",
                "189A Balham High Road",
                "200 Balham High Road",
            ]
        )
        self.assertEqual(set(addresses), expected)

    def test_station_ids(self):
        self.assertEqual(
            "5730",
            ResidentialAddress.objects.get(
                slug="x01000000-5730-189a-balham-high-road-sw129be"
            ).polling_station_id,
        )
        self.assertEqual(
            "5730",
            ResidentialAddress.objects.get(
                slug="x01000000-5730-189-balham-high-road-sw129be"
            ).polling_station_id,
        )
        self.assertEqual(
            "5736",
            ResidentialAddress.objects.get(
                slug="x01000000-5736-200-balham-high-road-sw177be"
            ).polling_station_id,
        )
        self.assertEqual(
            "5736",
            ResidentialAddress.objects.get(
                slug="x01000000-5736-balham-high-road-sw177be"
            ).polling_station_id,
        )

    def test_stations(self):
        stations = (
            PollingStation.objects.filter(council_id="X01000000")
            .order_by("internal_council_id")
            .values_list("address", flat=True)
        )

        # check we inserted 2 stations
        self.assertEqual(2, len(stations))
        expected = set(
            [
                "Upper Tooting Methodist Church\nBalham High Road\nLondon",
                "Southside Scout Centre\n197 Balham High Road\nLondon",
            ]
        )
        self.assertEqual(set(stations), expected)


class XpressWebLookupAmbiguousAddressTests(TestCase):

    opts = {"noclean": False, "nochecks": True, "verbosity": 0}

    def test_ambiguous(self):
        Council.objects.update_or_create(pk="X01000000")
        cmd = stub_xpress_weblookup.Command()
        cmd.addresses_name = "test_ambiguous.csv"
        cmd.stations_name = "test_ambiguous.csv"
        cmd.handle(**self.opts)

        # No records should be inserted when we import this
        # fixture due to ambiguous address checks
        addresses = ResidentialAddress.objects.filter(council_id="X01000000").order_by(
            "address"
        )
        self.assertEqual(0, len(addresses))
