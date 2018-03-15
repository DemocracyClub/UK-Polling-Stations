from data_collection.data_types import Address, AddressSet
from django.test import TestCase


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class AddressSetTest(TestCase):

    def test_add_with_duplicates(self):
        in_list = [
            {'address': 'foo', 'slug': 'foo', 'postcode': '', 'council': '', 'polling_station_id': '', 'uprn': '',},
            {'address': 'bar', 'slug': 'bar', 'postcode': '', 'council': '', 'polling_station_id': '', 'uprn': '',},
            {'address': 'foo', 'slug': 'foo', 'postcode': '', 'council': '', 'polling_station_id': '', 'uprn': '',},
        ]

        expected = set([
            Address(
                address='foo', slug='foo', postcode='', council='', polling_station_id='', uprn='', location=None),
            Address(
                address='bar', slug='bar', postcode='', council='', polling_station_id='', uprn='', location=None),
        ])

        address_list = AddressSet(MockLogger())
        for el in in_list:
            address_list.add(el)

        self.assertEqual(expected, address_list.elements)

    def test_remove_ambiguous_addresses_exactmatch(self):
        in_list = [
            {
                'address': 'Haringey Park, London',
                'postcode': 'N89JG',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'haringey-park-london-n89jg-aa',
                'uprn': '',
            },
            {
                'address': 'Haringey Park, London',
                'postcode': 'N89JG',
                'polling_station_id': 'AB',
                'council': '',
                'slug': 'haringey-park-london-n89jg-ab',
                'uprn': '',
            },
            {
                'address': 'Haringey Park, London',
                'postcode': 'N89JG',
                'polling_station_id': 'AC',
                'council': '',
                'slug': 'haringey-park-london-n89jg-ac',
                'uprn': '',
            },
        ]

        address_list = AddressSet(MockLogger())
        for el in in_list:
            address_list.add(el)
        result = address_list.remove_ambiguous_addresses()

        self.assertEqual(set(), result)

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
                'address': '5-6 Mickleton Dr, Southport',
                'postcode': 'PR82QX',
                'polling_station_id': 'A01',
                'council': '',
                'slug': 'a',
                'uprn': '',
            },
            {
                'address': '5/6, Mickleton Dr.  Southport',
                'postcode': 'PR82QX',
                'polling_station_id': 'A02',
                'council': '',
                'slug': 'b',
                'uprn': '',
            },
            {
                'address': '5-6 mickleton dr southport',
                'postcode': 'PR82QX',
                'polling_station_id': 'A03',
                'council': '',
                'slug': 'c',
                'uprn': '',
            },
            {
                'address': '56 Mickleton Dr, Southport',
                'postcode': 'PR82QX',
                'polling_station_id': 'A04',
                'council': '',
                'slug': 'd',
                'uprn': '',
            },
            {
                'address': '5-6 Mickleton Dr, Southport',
                'postcode': 'BT281QZ',
                'polling_station_id': 'A05',
                'council': '',
                'slug': 'e',
                'uprn': '',
            },
            {
                'address': '56 Mickleton Dr, Southport',
                'postcode': 'BT281QZ',
                'polling_station_id': 'A04',
                'council': '',
                'slug': 'f',
                'uprn': '',
            },
        ]

        expected = set([
            Address(
                address='5-6 Mickleton Dr, Southport',
                postcode='BT281QZ',
                polling_station_id='A05',
                council='',
                slug='e',
                uprn='',
                location=None),
            Address(
                address='56 Mickleton Dr, Southport',
                postcode='BT281QZ',
                polling_station_id='A04',
                council='',
                slug='f',
                uprn='',
                location=None),
        ])

        address_list = AddressSet(MockLogger())
        for el in in_list:
            address_list.add(el)
        result = address_list.remove_ambiguous_addresses()

        self.assertEqual(expected, result)

    def test_remove_ambiguous_addresses_some_stations_match(self):
        # if one polling station doesn't match, we should remove all of them
        in_list = [
            {
                'address': 'Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'a',
                'uprn': '',
            },
            {
                'address': 'Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'b',
                'uprn': '',
            },
            {
                'address': 'Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AB',
                'council': '',
                'slug': 'c',
                'uprn': '',
            },
            {
                'address': 'Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'd',
                'uprn': '',
            },
        ]

        address_list = AddressSet(MockLogger())
        for el in in_list:
            address_list.add(el)
        result = address_list.remove_ambiguous_addresses()

        self.assertEqual(set(), result)

    def test_remove_ambiguous_addresses_whole_postcode(self):
        # if we've got one ambiguous address,
        # we should remove all addresse with the same postcode
        in_list = [
            {
                'address': '1 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'a',
                'uprn': '',
            },
            {
                'address': '2 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'b',
                'uprn': '',
            },
            {
                'address': '3 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AB',
                'council': '',
                'slug': 'c',
                'uprn': '',
            },
            {
                'address': '3 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'd',
                'uprn': '',
            },
        ]

        address_list = AddressSet(MockLogger())
        for el in in_list:
            address_list.add(el)
        result = address_list.remove_ambiguous_addresses()

        self.assertEqual(set(), result)

    def test_remove_ambiguous_addresses_no_issues(self):
        # if there are no ambiguous addresses,
        # we shouldn't do anything

        in_list = [
            {
                'address': '1 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'a',
                'uprn': '',
            },
            {
                'address': '2 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'b',
                'uprn': '',
            },
            {
                'address': '3 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AB',
                'council': '',
                'slug': 'c',
                'uprn': '',
            },
            {
                'address': '4 Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'd',
                'uprn': '',
            },
        ]

        address_list = AddressSet(MockLogger())
        for el in in_list:
            address_list.add(el)
        expected = set(address_list.elements)
        result = address_list.remove_ambiguous_addresses()

        self.assertEqual(expected, result)
