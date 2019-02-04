from copy import deepcopy
from django.test import TestCase
from data_collection.data_types import AddressList


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class AddressListTest(TestCase):
    def test_add_with_duplicates(self):
        in_list = [
            {
                "address": "foo",
                "slug": "foo",
                "postcode": "AA11AA",
                "council": "X01000001",
                "polling_station_id": "01",
                "uprn": "",
            },
            {
                "address": "bar",
                "slug": "bar",
                "postcode": "AA11AA",
                "council": "X01000001",
                "polling_station_id": "01",
                "uprn": "",
            },
            {
                "address": "foo",
                "slug": "foo",
                "postcode": "AA11AA",
                "council": "X01000001",
                "polling_station_id": "01",
                "uprn": "",
            },
        ]

        expected = [
            {
                "address": "foo",
                "slug": "foo",
                "postcode": "AA11AA",
                "council": "X01000001",
                "polling_station_id": "01",
                "uprn": "",
            },
            {
                "address": "bar",
                "slug": "bar",
                "postcode": "AA11AA",
                "council": "X01000001",
                "polling_station_id": "01",
                "uprn": "",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(expected, address_list.elements)

    def test_remove_ambiguous_addresses_exactmatch(self):
        in_list = [
            {
                "address": "Haringey Park, London",
                "postcode": "N89JG",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "haringey-park-london-n89jg-aa",
                "uprn": "",
            },
            {
                "address": "Haringey Park, London",
                "postcode": "N89JG",
                "polling_station_id": "AB",
                "council": "X01000001",
                "slug": "haringey-park-london-n89jg-ab",
                "uprn": "",
            },
            {
                "address": "Haringey Park, London",
                "postcode": "N89JG",
                "polling_station_id": "AC",
                "council": "X01000001",
                "slug": "haringey-park-london-n89jg-ac",
                "uprn": "",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)
        address_list.remove_ambiguous_addresses_by_address()

        self.assertEqual([], address_list.elements)

    def test_remove_ambiguous_addresses_fuzzymatch(self):
        """
        The addresses:
        - 5-6 Mickleton Dr, Southport, PR82QX
        - 5/6, Mickleton Dr.  Southport, PR82QX
        - 5-6 mickleton dr southport, PR82QX
        should all be considered the same address.

        The addresses:
        - 56 Mickleton Dr, Southport, PR82QX
        - 5-6 Mickleton Dr, Southport, BT281QZ
        should be identified as different.
        """
        in_list = [
            {
                "address": "5-6 Mickleton Dr, Southport",
                "postcode": "PR82QX",
                "polling_station_id": "A01",
                "council": "X01000001",
                "slug": "a",
                "uprn": "",
            },
            {
                "address": "5/6, Mickleton Dr.  Southport",
                "postcode": "PR82QX",
                "polling_station_id": "A02",
                "council": "X01000001",
                "slug": "b",
                "uprn": "",
            },
            {
                "address": "5-6 mickleton dr southport",
                "postcode": "PR82QX",
                "polling_station_id": "A03",
                "council": "X01000001",
                "slug": "c",
                "uprn": "",
            },
            {
                "address": "56 Mickleton Dr, Southport",
                "postcode": "PR82QX",
                "polling_station_id": "A04",
                "council": "X01000001",
                "slug": "d",
                "uprn": "",
            },
            {
                "address": "5-6 Mickleton Dr, Southport",
                "postcode": "BT281QZ",
                "polling_station_id": "A05",
                "council": "X01000001",
                "slug": "e",
                "uprn": "",
            },
            {
                "address": "56 Mickleton Dr, Southport",
                "postcode": "BT281QZ",
                "polling_station_id": "A04",
                "council": "X01000001",
                "slug": "f",
                "uprn": "",
            },
        ]

        expected = [
            {
                "address": "5-6 Mickleton Dr, Southport",
                "postcode": "BT281QZ",
                "polling_station_id": "A05",
                "council": "X01000001",
                "slug": "e",
                "uprn": "",
            },
            {
                "address": "56 Mickleton Dr, Southport",
                "postcode": "BT281QZ",
                "polling_station_id": "A04",
                "council": "X01000001",
                "slug": "f",
                "uprn": "",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)
        address_list.remove_ambiguous_addresses_by_address()

        self.assertEqual(expected, address_list.elements)

    def test_remove_ambiguous_addresses_some_stations_match(self):
        # if one polling station doesn't match, we should remove all of them
        in_list = [
            {
                "address": "Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "a",
                "uprn": "",
            },
            {
                "address": "Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "b",
                "uprn": "",
            },
            {
                "address": "Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AB",
                "council": "X01000001",
                "slug": "c",
                "uprn": "",
            },
            {
                "address": "Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "d",
                "uprn": "",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(4, len(address_list.elements))
        address_list.remove_ambiguous_addresses_by_address()
        self.assertEqual([], address_list.elements)

    def test_remove_ambiguous_addresses_whole_postcode(self):
        # if we've got one ambiguous address,
        # we should remove all addresse with the same postcode
        in_list = [
            {
                "address": "1 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "a",
                "uprn": "",
            },
            {
                "address": "2 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "b",
                "uprn": "",
            },
            {
                "address": "3 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AB",
                "council": "X01000001",
                "slug": "c",
                "uprn": "",
            },
            {
                "address": "3 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "d",
                "uprn": "",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(4, len(address_list.elements))
        address_list.remove_ambiguous_addresses_by_address()
        self.assertEqual([], address_list.elements)

    def test_remove_ambiguous_addresses_no_issues(self):
        # if there are no ambiguous addresses,
        # we shouldn't do anything

        in_list = [
            {
                "address": "1 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "a",
                "uprn": "",
            },
            {
                "address": "2 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "b",
                "uprn": "",
            },
            {
                "address": "3 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AB",
                "council": "X01000001",
                "slug": "c",
                "uprn": "",
            },
            {
                "address": "4 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "d",
                "uprn": "",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        expected = deepcopy(address_list.elements)
        address_list.remove_ambiguous_addresses_by_address()
        self.assertEqual(expected, address_list.elements)

    def test_attach_doorstep_grid_refs(self):
        in_list = [
            {
                "address": "1 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "a",
                "uprn": "00001",
            },
            {
                "address": "4 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "d",
                "uprn": "00004",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        addressbase = {
            # 00001 is in here but 00004 isn't
            "00001": {"location": "SRID=4326;POINT(-0.9288492 53.3119342)"}
        }

        address_list.attach_doorstep_gridrefs(addressbase)

        self.assertEqual(2, len(address_list.elements))
        for el in address_list.elements:
            if el["uprn"] == "00001":
                self.assertEqual(
                    "SRID=4326;POINT(-0.9288492 53.3119342)", el["location"]
                )
            if el["uprn"] == "00004":
                self.assertEqual(None, el.get("location", None))

    def test_remove_invalid_uprns(self):
        in_list = [
            {
                "address": "1 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "a",
                "uprn": "00001",
            },
            {
                "address": "2 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "b",
                "uprn": "00002",
            },
            {
                "address": "3 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AB",
                "council": "X01000001",
                "slug": "c",
                "uprn": "00003",
            },
            {
                "address": "4 Abbeyvale Dr, Liverpool",
                "postcode": "L252NW",
                "polling_station_id": "AA",
                "council": "X01000001",
                "slug": "d",
                "uprn": "00004",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        addressbase = {
            "00001": {
                "postcode": "L252NW",
                "address": "1 Abbeyvale Dr, Liverpool",
                "location": "SRID=4326;POINT(-0.9288492 53.3119342)",
            },
            "00002": {
                "postcode": "L252NW",
                "address": "2 Abbeyvale Dr, Liverpool",
                "location": "SRID=4326;POINT(-0.9288480 53.3119345)",
            },
            "00003": {
                "postcode": "L252XX",  # this postcode doesn't match with the input record
                "address": "2 Abbeyvale Dr, Liverpool",
                "location": "SRID=4326;POINT(-0.9288400 53.3119332)",
            }
            # 00004 is not in here
        }

        address_list.remove_invalid_uprns(addressbase)

        # 00003 and 00004 should still be in the set
        self.assertEqual(4, len(address_list.elements))
        # but those records should now have a blank uprn
        for el in address_list.elements:
            assert el["uprn"] in ["00001", "00002", ""]
