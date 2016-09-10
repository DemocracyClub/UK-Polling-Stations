from data_collection.custom_lists import AddressList
from django.test import TestCase


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class AddressListTest(TestCase):

    def test_add_with_duplicates(self):
        in_list = [
            {'address': 'foo', 'slug': 'foo'},
            {'address': 'bar', 'slug': 'bar'},
            {'address': 'foo', 'slug': 'foo'},
        ]

        expected = [
            {'address': 'foo', 'slug': 'foo'},
            {'address': 'bar', 'slug': 'bar'},
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(expected, address_list.elements)

    def test_remove_ambiguous_addresses_exactmatch(self):
        in_list = [
            {'address': 'Haringey Park, London', 'postcode': 'N89JG', 'polling_station_id': 'AA'},
            {'address': 'Haringey Park, London', 'postcode': 'N89JG', 'polling_station_id': 'AB'},
            {'address': 'Haringey Park, London', 'postcode': 'N89JG', 'polling_station_id': 'AC'},
        ]

        address_list = AddressList(MockLogger())
        result = address_list.remove_ambiguous_addresses(in_list)

        self.assertEqual([], result)

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
            {'address': '5-6 Mickleton Dr, Southport',   'postcode': 'PR82QX',  'polling_station_id': 'A01'},
            {'address': '5/6, Mickleton Dr.  Southport', 'postcode': 'PR82QX',  'polling_station_id': 'A02'},
            {'address': '5-6 mickleton dr southport',    'postcode': 'PR82QX',  'polling_station_id': 'A03'},
            {'address': '56 Mickleton Dr, Southport',    'postcode': 'PR82QX',  'polling_station_id': 'A04'},
            {'address': '5-6 Mickleton Dr, Southport',   'postcode': 'BT281QZ', 'polling_station_id': 'A05'}
        ]

        address_list = AddressList(MockLogger())
        result = address_list.remove_ambiguous_addresses(in_list)

        self.assertEqual(2, len(result))
        self.assertEqual('56 Mickleton Dr, Southport', result[0]['address'])
        self.assertEqual('PR82QX', result[0]['postcode'])
        self.assertEqual('5-6 Mickleton Dr, Southport', result[1]['address'])
        self.assertEqual('BT281QZ', result[1]['postcode'])

    def test_remove_ambiguous_addresses_some_stations_match(self):
        # if one polling station doesn't match, we should remove all of them
        in_list = [
            {'address': 'Abbeyvale Dr, Liverpool', 'postcode': 'L252NW', 'polling_station_id': 'AA'},
            {'address': 'Abbeyvale Dr, Liverpool', 'postcode': 'L252NW', 'polling_station_id': 'AA'},
            {'address': 'Abbeyvale Dr, Liverpool', 'postcode': 'L252NW', 'polling_station_id': 'AB'},
            {'address': 'Abbeyvale Dr, Liverpool', 'postcode': 'L252NW', 'polling_station_id': 'AA'},
        ]

        address_list = AddressList(MockLogger())
        result = address_list.remove_ambiguous_addresses(in_list)

        self.assertEqual([], result)
