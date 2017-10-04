from collections import namedtuple
from django.test import TestCase
from uk_geo_utils.helpers import AddressSorter

Address = namedtuple('Address', ['id', 'address'])

class AddressSorterTest(TestCase):

    def test_numeric_order(self):
        # Addresses should sort in numeric order, not string order
        in_list = [
            Address(id=1, address="10, THE SQUARE, BOGNOR REGIS"),
            Address(id=2, address="1, THE SQUARE, BOGNOR REGIS"),
            Address(id=3, address="2, THE SQUARE, BOGNOR REGIS"),
        ]

        expected = [
            Address(id=2, address="1, THE SQUARE, BOGNOR REGIS"),
            Address(id=3, address="2, THE SQUARE, BOGNOR REGIS"),
            Address(id=1, address="10, THE SQUARE, BOGNOR REGIS"),
        ]

        sorter = AddressSorter(in_list)
        result = sorter.natural_sort()

        self.assertEqual(expected, result)

    def test_group_by_street(self):
        # Numbered addresses should group by street/building
        in_list = [
            Address(id=1, address="1  Haynes House Mount Pleasant"),
            Address(id=2, address="1  Partridge House Mount Pleasant"),
            Address(id=3, address="3  Haynes House Mount Pleasant"),
            Address(id=4, address="2  Partridge House Mount Pleasant"),
            Address(id=5, address="2  Haynes House Mount Pleasant"),
        ]

        expected = [
            Address(id=1, address="1  Haynes House Mount Pleasant"),
            Address(id=5, address="2  Haynes House Mount Pleasant"),
            Address(id=3, address="3  Haynes House Mount Pleasant"),
            Address(id=2, address="1  Partridge House Mount Pleasant"),
            Address(id=4, address="2  Partridge House Mount Pleasant"),
        ]

        sorter = AddressSorter(in_list)
        result = sorter.natural_sort()

        self.assertEqual(expected, result)

    def test_group_in_numbered_buildings(self):
        # Numbered addresses should group inside numbered buildings
        in_list = [
            Address(id=1, address="1  Southlands Court Birchfield Road"),
            Address(id=2, address="1 233 The Beeches Birchfield Road"),
            Address(id=3, address="207 Birchfield Road"),
            Address(id=4, address="203 Birchfield Road"),
            Address(id=5, address="2 233 The Beeches Birchfield Road"),
            Address(id=6, address="2  Southlands Court Birchfield Road"),
        ]

        expected = [
            Address(id=2, address="1 233 The Beeches Birchfield Road"),
            Address(id=5, address="2 233 The Beeches Birchfield Road"),
            Address(id=1, address="1  Southlands Court Birchfield Road"),
            Address(id=6, address="2  Southlands Court Birchfield Road"),
            Address(id=4, address="203 Birchfield Road"),
            Address(id=3, address="207 Birchfield Road"),
        ]

        sorter = AddressSorter(in_list)
        result = sorter.natural_sort()

        self.assertEqual(expected, result)

    def test_number_suffix(self):
        # Numbered addresses with number suffix should sort in
        # numeric order and then alphabetically by suffix
        in_list = [
            Address(id=1, address="200A Evesham Road"),
            Address(id=2, address="190A Evesham Road"),
            Address(id=3, address="The Forge Mill Evesham Road"),
            Address(id=4, address="202A Evesham Road"),
            Address(id=5, address="190C Evesham Road"),
            Address(id=6, address="190B Evesham Road"),
        ]

        expected = [
            Address(id=2, address="190A Evesham Road"),
            Address(id=6, address="190B Evesham Road"),
            Address(id=5, address="190C Evesham Road"),
            Address(id=1, address="200A Evesham Road"),
            Address(id=4, address="202A Evesham Road"),
            Address(id=3, address="The Forge Mill Evesham Road"),
        ]

        sorter = AddressSorter(in_list)
        result = sorter.natural_sort()

        self.assertEqual(expected, result)

    def test_prefixed_numbers(self):
        # Prefixed numbers (e.g: flats) should sort by number
        in_list = [
            Address(id=1, address="Flat 10  Knapton House North Walsham Road"),
            Address(id=2, address="Gardeners Cottage   Knapton House North Walsham Road"),
            Address(id=3, address="Old Coach House North Walsham Road"),
            Address(id=4, address="Flat 1  Knapton House North Walsham Road"),
            Address(id=5, address="Flat 2  Knapton House North Walsham Road"),
        ]

        expected = [
            Address(id=4, address="Flat 1  Knapton House North Walsham Road"),
            Address(id=5, address="Flat 2  Knapton House North Walsham Road"),
            Address(id=1, address="Flat 10  Knapton House North Walsham Road"),
            Address(id=2, address="Gardeners Cottage   Knapton House North Walsham Road"),
            Address(id=3, address="Old Coach House North Walsham Road"),
        ]

        sorter = AddressSorter(in_list)
        result = sorter.natural_sort()

        self.assertEqual(expected, result)
