import datetime as dt
from unittest import TestCase
from polling_stations.apps.core.templatetags.date_filters import human_date


class TestDateFilters(TestCase):
    def test_human_date_with_date(self):
        date_value = dt.date(2024, 6, 15)
        formatted_date = human_date(date_value)
        self.assertEqual(formatted_date, "15 June 2024")

    def test_human_date_with_datetime(self):
        datetime_value = dt.datetime(2024, 6, 15, 12, 0)
        formatted_date = human_date(datetime_value)
        self.assertEqual(formatted_date, "15 June 2024")

    def test_human_date_with_string_valid(self):
        string_value = "2024-06-15"
        formatted_date = human_date(string_value)
        self.assertEqual(formatted_date, "15 June 2024")

    def test_human_date_with_string_invalid(self):
        string_value = "buttons"
        formatted_date = human_date(string_value)
        self.assertEqual(formatted_date, "buttons")
