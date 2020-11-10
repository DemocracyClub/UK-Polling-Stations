from django.contrib.gis.geos import Point
from django.test import TestCase

from data_importers.base_importers import BaseStationsDistrictsImporter
from data_importers.data_types import StationSet, DistrictSet


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class BaseStationsDistrictsImporterTest(TestCase):
    def setUp(self):
        self.importer = BaseStationsDistrictsImporter
        self.importer.__abstractmethods__ = set()
        self.importer = self.importer()
        self.importer.logger = MockLogger()
        self.importer.verbosity = 0
        self.importer.stations = StationSet()
        self.importer.districts = DistrictSet()

    def test_stations_have_district_ids(self):
        self.importer.stations.add(
            {
                "council": "foo",
                "internal_council_id": "ABC",
                "polling_district_id": "XYZ",
            }
        )
        self.importer.districts.add(
            {
                "council": "foo",
                "internal_council_id": "XYZ",
                "polling_station_id": "",
                "area": Point(0, 0),
            }
        )

        self.assertFalse(self.importer.districts_have_station_ids)

    def test_districts_have_station_ids(self):
        self.importer.stations.add(
            {
                "council": "foo",
                "internal_council_id": "ABC",
                "polling_district_id": "",
            }
        )
        self.importer.districts.add(
            {
                "council": "foo",
                "internal_council_id": "XYZ",
                "polling_station_id": "ABC",
                "area": Point(0, 0),
            }
        )

        self.assertTrue(self.importer.districts_have_station_ids)
