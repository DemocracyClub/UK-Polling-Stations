from operator import itemgetter
from django.test import TestCase
from data_finder.helpers import AddressSorter

class AddressSorterTest(TestCase):

    def setUp(self):
        self.sorter = AddressSorter()
        self.key = itemgetter(1)

    def test_numeric_order(self):
        # Addresses should sort in numeric order, not string order
        in_list = [
            (1, "10, THE SQUARE, BOGNOR REGIS"),
            (2, "1, THE SQUARE, BOGNOR REGIS"),
            (3, "2, THE SQUARE, BOGNOR REGIS"),
        ]

        expected = [
            (2, "1, THE SQUARE, BOGNOR REGIS"),
            (3, "2, THE SQUARE, BOGNOR REGIS"),
            (1, "10, THE SQUARE, BOGNOR REGIS"),
        ]

        result = self.sorter.natural_sort(in_list, self.key)

        self.assertEqual(expected, result)

    def test_group_by_street(self):
        # Numbered addresses should group by street/building
        in_list = [
            (1, "1  Haynes House Mount Pleasant"),
            (2, "1  Partridge House Mount Pleasant"),
            (3, "3  Haynes House Mount Pleasant"),
            (4, "2  Partridge House Mount Pleasant"),
            (5, "2  Haynes House Mount Pleasant"),
        ]

        expected = [
            (1, "1  Haynes House Mount Pleasant"),
            (5, "2  Haynes House Mount Pleasant"),
            (3, "3  Haynes House Mount Pleasant"),
            (2, "1  Partridge House Mount Pleasant"),
            (4, "2  Partridge House Mount Pleasant"),
        ]

        result = self.sorter.natural_sort(in_list, self.key)

        self.assertEqual(expected, result)

    def test_group_in_numbered_buildings(self):
        # Numbered addresses should group inside numbered buildings
        in_list = [
            (1, "1  Southlands Court Birchfield Road"),
            (2, "1 233 The Beeches Birchfield Road"),
            (3, "207 Birchfield Road"),
            (4, "203 Birchfield Road"),
            (5, "2 233 The Beeches Birchfield Road"),
            (6, "2  Southlands Court Birchfield Road"),
        ]

        expected = [
            (2, "1 233 The Beeches Birchfield Road"),
            (5, "2 233 The Beeches Birchfield Road"),
            (1, "1  Southlands Court Birchfield Road"),
            (6, "2  Southlands Court Birchfield Road"),
            (4, "203 Birchfield Road"),
            (3, "207 Birchfield Road"),
        ]

        result = self.sorter.natural_sort(in_list, self.key)

        self.assertEqual(expected, result)

    def test_number_suffix(self):
        # Numbered addresses with number suffix should sort in
        # numeric order and then alphabetically by suffix
        in_list = [
            (1, "200A Evesham Road"),
            (2, "190A Evesham Road"),
            (3, "The Forge Mill Evesham Road"),
            (4, "202A Evesham Road"),
            (5, "190C Evesham Road"),
            (6, "190B Evesham Road"),
        ]

        expected = [
            (2, "190A Evesham Road"),
            (6, "190B Evesham Road"),
            (5, "190C Evesham Road"),
            (1, "200A Evesham Road"),
            (4, "202A Evesham Road"),
            (3, "The Forge Mill Evesham Road"),
        ]

        result = self.sorter.natural_sort(in_list, self.key)

        self.assertEqual(expected, result)

    def test_prefixed_numbers(self):
        # Prefixed numbers (e.g: flats) should sort by number
        in_list = [
            (1, "Flat 10  Knapton House North Walsham Road"),
            (2, "Gardeners Cottage   Knapton House North Walsham Road"),
            (3, "Old Coach House North Walsham Road"),
            (4, "Flat 1  Knapton House North Walsham Road"),
            (5, "Flat 2  Knapton House North Walsham Road"),
        ]

        expected = [
            (4, "Flat 1  Knapton House North Walsham Road"),
            (5, "Flat 2  Knapton House North Walsham Road"),
            (1, "Flat 10  Knapton House North Walsham Road"),
            (2, "Gardeners Cottage   Knapton House North Walsham Road"),
            (3, "Old Coach House North Walsham Road"),
        ]

        result = self.sorter.natural_sort(in_list, self.key)

        self.assertEqual(expected, result)
