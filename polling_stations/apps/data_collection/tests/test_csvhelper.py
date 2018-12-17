import os
from django.test import TestCase
from data_collection.filehelpers import CsvHelper


class CsvHelperTest(TestCase):
    def test_parse_csv(self):
        helper = CsvHelper(
            os.path.join(os.path.dirname(__file__), "fixtures/csv_helper/test.csv")
        )
        data = helper.get_features()

        self.assertIsInstance(data[0], tuple)
        self.assertEqual("1", data[0].foo)
        self.assertEqual("2", data[0].b_a_r)
        self.assertEqual("3", data[0].baz)

        self.assertIsInstance(data[1], tuple)
        self.assertEqual("cheese", data[1].foo)
        self.assertEqual("peas", data[1].b_a_r)
        self.assertEqual("", data[1].baz)

        self.assertNotIn(2, data)
