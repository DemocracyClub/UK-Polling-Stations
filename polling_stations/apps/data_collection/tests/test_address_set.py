from data_collection.data_types import Address, AddressSet
from django.test import TestCase


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class AddressSetTest(TestCase):

    def test_add_with_duplicates(self):
        in_list = [
            {'address': 'foo', 'slug': 'foo', 'postcode': '', 'council': '', 'polling_station_id': ''},
            {'address': 'bar', 'slug': 'bar', 'postcode': '', 'council': '', 'polling_station_id': ''},
            {'address': 'foo', 'slug': 'foo', 'postcode': '', 'council': '', 'polling_station_id': ''},
        ]

        expected = set([
            Address(
                address='foo', slug='foo', postcode='', council='', polling_station_id=''),
            Address(
                address='bar', slug='bar', postcode='', council='', polling_station_id=''),
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
                'slug': 'haringey-park-london-n89jg-aa'
            },
            {
                'address': 'Haringey Park, London',
                'postcode': 'N89JG',
                'polling_station_id': 'AB',
                'council': '',
                'slug': 'haringey-park-london-n89jg-ab'
            },
            {
                'address': 'Haringey Park, London',
                'postcode': 'N89JG',
                'polling_station_id': 'AC',
                'council': '',
                'slug': 'haringey-park-london-n89jg-ac'
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
                'slug': 'a'
            },
            {
                'address': '5/6, Mickleton Dr.  Southport',
                'postcode': 'PR82QX',
                'polling_station_id': 'A02',
                'council': '',
                'slug': 'b'
            },
            {
                'address': '5-6 mickleton dr southport',
                'postcode': 'PR82QX',
                'polling_station_id': 'A03',
                'council': '',
                'slug': 'c'
            },
            {
                'address': '56 Mickleton Dr, Southport',
                'postcode': 'PR82QX',
                'polling_station_id': 'A04',
                'council': '',
                'slug': 'd'
            },
            {
                'address': '5-6 Mickleton Dr, Southport',
                'postcode': 'BT281QZ',
                'polling_station_id': 'A05',
                'council': '',
                'slug': 'e'
            },
        ]

        expected = set([
            Address(
                address='56 Mickleton Dr, Southport',
                postcode='PR82QX',
                polling_station_id='A04',
                council='',
                slug='d'),
            Address(
                address='5-6 Mickleton Dr, Southport',
                postcode='BT281QZ',
                polling_station_id='A05',
                council='',
                slug='e'),
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
                'slug': 'a'
            },
            {
                'address': 'Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'b'
            },
            {
                'address': 'Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AB',
                'council': '',
                'slug': 'c'
            },
            {
                'address': 'Abbeyvale Dr, Liverpool',
                'postcode': 'L252NW',
                'polling_station_id': 'AA',
                'council': '',
                'slug': 'd'
            },
        ]

        address_list = AddressSet(MockLogger())
        for el in in_list:
            address_list.add(el)
        result = address_list.remove_ambiguous_addresses()

        self.assertEqual(set(), result)
