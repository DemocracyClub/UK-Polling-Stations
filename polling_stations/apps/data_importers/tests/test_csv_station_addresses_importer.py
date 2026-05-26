from data_importers.base_importers import BaseCsvStationsCsvAddressesImporter
from django.test import TestCase
from collections import namedtuple
from unittest.mock import patch, Mock

StubStationRecord = namedtuple(
    "StubStationRecord",
    [
        "station_id_field",
        "station_postcode_field",
        "station_easting_field",
        "station_northing_field",
        "station_uprn_field",
    ],
)


class BaseCsvStationsCsvAddressesImporterTests(TestCase):
    def setUp(self):
        self.importer = BaseCsvStationsCsvAddressesImporter
        self.importer.__abstractmethods__ = set()
        self.importer = self.importer()

        self.test_record = StubStationRecord(
            station_id_field="test_id",
            station_postcode_field="AA1 1AA",
            station_easting_field="530264",
            station_northing_field="179650",
            station_uprn_field="123456789",
        )

    def test_get_station_id_missing_field(self):
        station_id = self.importer.get_station_id(self.test_record)
        self.assertEqual(station_id, None)

    def test_get_station_id(self):
        self.importer.station_id_field = "station_id_field"

        station_id = self.importer.get_station_id(self.test_record)
        self.assertEqual(station_id, self.test_record.station_id_field)

    def test_get_station_uprn(self):
        self.importer.station_uprn_field = "station_uprn_field"

        station_uprn = self.importer.get_station_uprn(self.test_record)
        self.assertEqual(station_uprn, self.test_record.station_uprn_field)

    def test_get_station_uprn_missing_field(self):
        station_uprn = self.importer.get_station_uprn(self.test_record)
        self.assertEqual(station_uprn, None)

    def test_get_station_coordinates(self):
        self.importer.station_easting_field = "station_easting_field"
        self.importer.station_northing_field = "station_northing_field"

        easting, northing = self.importer.get_station_coordinates(self.test_record)
        self.assertEqual(easting, self.test_record.station_easting_field)
        self.assertEqual(northing, self.test_record.station_northing_field)

    def test_get_station_coordinates_missing_fields(self):
        coords = self.importer.get_station_coordinates(self.test_record)
        self.assertEqual(coords, None)

    def test_get_station_postcode(self):
        self.importer.station_postcode_field = "station_postcode_field"

        station_postcode = self.importer.get_station_postcode(self.test_record)
        self.assertEqual(station_postcode, self.test_record.station_postcode_field)

    def test_get_station_postcode_missing_field(self):
        station_postcode = self.importer.get_station_postcode(self.test_record)
        self.assertEqual(station_postcode, None)

    @patch("data_importers.base_importers.geocode_point_only")
    def test_geocode_from_postcode(self, mock_geocode_point_only):
        mock_point = Mock()
        mock_point.centroid = "geocoded_location"
        mock_geocode_point_only.return_value = mock_point
        station_postcode = self.test_record.station_postcode_field

        location = self.importer.geocode_from_postcode(station_postcode)

        mock_geocode_point_only.assert_called_once_with(station_postcode)
        self.assertEqual(location, "geocoded_location")
