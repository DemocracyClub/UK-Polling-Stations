import os
from unittest.mock import patch

from councils.tests.factories import CouncilFactory
from data_importers.base_importers import BaseStationsImporter
from data_importers.data_types import StationSet
from django.contrib.gis.geos import Point
from django.test import TestCase


class MockLogger:
    logs = []

    def log_message(self, level, message, variable=None, pretty=False):
        self.logs.append(message)

    def clear_logs(self):
        self.logs = []


class BaseStationsImporterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.council = CouncilFactory()

    @patch(
        "data_importers.base_importers.BaseStationsImporter.__abstractmethods__", set()
    )
    def setUp(self):
        self.base_stations_importer = BaseStationsImporter()
        self.base_stations_importer.stations = StationSet()
        self.base_stations_importer.logger = MockLogger()

    def tearDown(self):
        pass

    def test_check_duplicate_location(self):
        ps1 = {
            "council": self.council.council_id,
            "internal_council_id": "01",
            "postcode": "AA11AA",
            "location": Point(y=50.62735, x=-3.98326, srid=4326),
            "address": "foo",
        }
        ps2 = {
            "council": self.council.council_id,
            "internal_council_id": "02",
            "postcode": "BB11BB",
            "location": Point(y=50.62735, x=-3.98326, srid=4326),
            "address": "bar",
        }
        ps3 = {
            "council": self.council.council_id,
            "internal_council_id": "03",
            "postcode": "CC11CC",
            "location": Point(y=82727, x=259821, srid=27700),
            "address": "baz",
        }
        self.base_stations_importer.add_polling_station(ps1)
        self.base_stations_importer.check_duplicate_location(ps2)
        self.assertListEqual(
            self.base_stations_importer.logger.logs,
            [
                "Polling stations 'bar' and 'foo' are at approximately the same location, "
                "but have different postcodes:\nqgis filter exp: \"internal_council_id\" IN ('02','01')"
            ],
        )
        if os.environ.get("CIRCLECI"):
            self.base_stations_importer.logger.clear_logs()
            self.base_stations_importer.check_duplicate_location(ps3)
            self.assertListEqual(
                self.base_stations_importer.logger.logs,
                [
                    "Polling stations 'baz' and 'foo' are at approximately the same location, "
                    "but have different postcodes:\nqgis filter exp: \"internal_council_id\" IN ('03','01')"
                ],
            )
