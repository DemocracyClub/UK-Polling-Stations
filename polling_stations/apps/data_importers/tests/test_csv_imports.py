from addressbase.models import Address, UprnToCouncil
from councils.tests.factories import CouncilFactory
from data_importers.tests.stubs import stub_addressimport
from django.test import TestCase


# High-level functional tests for import scripts
class ImporterTest(TestCase):
    opts = {"nochecks": True, "verbosity": 0, "include_past_elections": True}

    def set_up(self, addressbase, uprns, addresses_name):
        for address in addressbase:
            Address.objects.update_or_create(**address)

        for uprn in uprns:
            UprnToCouncil.objects.update_or_create(pk=uprn, lad="X01000000")

        CouncilFactory(pk="ABC", identifiers=["X01000000"])

        cmd = stub_addressimport.Command()
        cmd.addresses_name = addresses_name
        cmd.handle(**self.opts)

    def test_duplicate_uprns(self):
        """
        In the csv there are two matching uprns with different polling station ids.
        Despite one appearing in addressbase, neither should be imported.
        """
        test_params = {
            "uprns": ["1", "2", "6"],
            "addressbase": [
                {
                    "address": "Another Haringey Park, London",
                    "uprn": "1",
                    "postcode": "N8 8NM",
                },
                {"address": "Haringey Park, London", "uprn": "2", "postcode": "N8 9JG"},
                {
                    "address": "80 Pine Vale Cres, Bournemouth",
                    "uprn": "6",
                    "postcode": "BH10 6BJ",
                },
            ],
            "addresses_name": "duplicate_uprns.csv",
        }
        self.set_up(**test_params)

        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )
        self.assertEqual(1, len(imported_uprns))
        expected = {("6", "2")}
        self.assertEqual(set(imported_uprns), expected)

    def test_uprn_not_in_addressbase(self):
        """uprn does not appear in addressbase data, or in UprnToCouncil table"""
        test_params = {
            "uprns": ["6"],
            "addressbase": [
                {"address": "3 Factory Rd, Poole", "uprn": "4", "postcode": "BH16 5HT"},
                {
                    "address": "80 Pine Vale Cres, Bournemouth",
                    "uprn": "6",
                    "postcode": "BH10 6BJ",
                },
            ],
            "addresses_name": "uprn_missing.csv",
        }
        self.set_up(**test_params)

        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )
        self.assertEqual(1, len(imported_uprns))
        expected = {("6", "2")}
        self.assertEqual(set(imported_uprns), expected)

    def test_uprn_assigned_to_wrong_council(self):
        """Uprn exists but we've located it in a different council in UprnToCouncil table"""
        test_params = {
            "uprns": ["6"],
            "addressbase": [
                {"address": "3 Factory Rd, Poole", "uprn": "4", "postcode": "BH16 5HT"},
                {
                    "address": "80 Pine Vale Cres, Bournemouth",
                    "uprn": "6",
                    "postcode": "BH10 6BJ",
                },
            ],
            "addresses_name": "uprn_missing.csv",
        }
        self.set_up(**test_params)

        UprnToCouncil.objects.update_or_create(pk=4, lad="X01000002")

        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )
        self.assertEqual(1, len(imported_uprns))
        expected = {("6", "2")}
        self.assertEqual(set(imported_uprns), expected)

    def test_postcode_mismatch(self):
        """Uprn exists but postcodes don't match"""
        test_params = {
            "uprns": ["4", "7"],
            "addressbase": [
                {"address": "3 Factory Rd, Poole", "uprn": "4", "postcode": "BH16 5HT"},
                {
                    "address": "4 Factory Rd, Poole",
                    "uprn": "7",
                    "postcode": "BH16 5HT",  # postcode is 'BH17 5HT' in csv
                },
            ],
            "addresses_name": "uprn_missing.csv",
        }
        self.set_up(**test_params)

        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )
        self.assertEqual(1, len(imported_uprns))
        expected = {("4", "1")}
        self.assertEqual(set(imported_uprns), expected)

    def test_address_import(self):
        test_params = {
            "uprns": ["1", "3", "4", "5", "6", "7"],
            "addressbase": [
                {"address": "Haringey Park, London", "uprn": "1", "postcode": "N8 9JG"},
                # uprn '2' in addresses.csv but wasn't in addressbase so not in uprntocouncil either
                {
                    "address": "36 Abbots Park, London",
                    "uprn": "3",
                    "postcode": "SW2 3QD",
                },
                {"address": "3 Factory Rd, Poole", "uprn": "4", "postcode": "BH16 5HT"},
                {
                    "address": "5-6 Mickleton Dr, Southport",
                    "uprn": "5",
                    "postcode": "PR8 2QX",
                },
                {
                    "address": "80 Pine Vale Cres, Bournemouth",
                    "uprn": "6",
                    "postcode": "BH10 6BJ",
                },
                {
                    "address": "4 Factory Rd, Poole",
                    "uprn": "7",
                    "postcode": "BH16 5HT",  # postcode is 'BH17 5HT' in csv
                },
            ],
            "addresses_name": "addresses.csv",
        }
        self.set_up(**test_params)

        imported_uprns = (
            UprnToCouncil.objects.filter(lad="X01000000")
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )

        self.assertEqual(3, len(imported_uprns))
        expected = {("3", "3"), ("4", "1"), ("6", "2")}
        self.assertEqual(set(imported_uprns), expected)
