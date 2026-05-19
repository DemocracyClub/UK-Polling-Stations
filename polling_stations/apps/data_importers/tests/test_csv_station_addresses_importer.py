from data_importers.base_importers import BaseCsvStationsCsvAddressesImporter
from django.test import TestCase
from collections import namedtuple
from unittest.mock import patch
from pollingstations.models import LocationSourceChoices


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class BaseCsvStationsCsvAddressesImporterGetStationPointTests(TestCase):
    def setUp(self):
        self.importer = BaseCsvStationsCsvAddressesImporter
        self.importer.__abstractmethods__ = set()
        self.importer = self.importer()
        self.importer.logger = MockLogger()

        # Set generic station field names for testing
        self.importer.station_easting_field = "station_easting_field"
        self.importer.station_northing_field = "station_northing_field"
        self.importer.station_uprn_field = "station_uprn_field"
        self.importer.station_postcode_field = "station_postcode_field"
        self.importer.station_id_field = "station_id_field"
        self.importer.allow_station_point_from_postcode = False

        self.stub_station_record = namedtuple(
            "StubStationRecord",
            [
                "station_id_field",
                "station_postcode_field",
                "station_easting_field",
                "station_northing_field",
                "station_uprn_field",
            ],
        )

    def test_get_station_point_no_location_data(self):
        test_record = self.stub_station_record(
            station_id_field="001",
            station_postcode_field="postcode",
            station_easting_field="0",
            station_northing_field="0",
            station_uprn_field="",
        )
        location, location_source = self.importer.get_station_point(test_record)
        self.assertIsNone(location)
        self.assertEqual(location_source, LocationSourceChoices.NONE)

    @patch(
        "data_importers.base_importers.BaseCsvStationsCsvAddressesImporter.geocode_from_postcode",
    )
    def test_get_station_point_with_postcode(self, mock_postcode_geocode):
        mock_postcode_geocode.return_value = "geocoded_location"
        self.importer.allow_station_point_from_postcode = True

        test_record = self.stub_station_record(
            station_id_field="001",
            station_postcode_field="postcode",
            station_easting_field="0",
            station_northing_field="0",
            station_uprn_field="",
        )
        location, location_source = self.importer.get_station_point(test_record)
        mock_postcode_geocode.assert_called_once_with(test_record)
        self.assertEqual(location, mock_postcode_geocode.return_value)
        self.assertEqual(location_source, LocationSourceChoices.POSTCODE)

    @patch(
        "data_importers.base_importers.BaseCsvStationsCsvAddressesImporter.geocode_from_coordinates",
    )
    def test_get_station_point_with_coordinates(self, mock_coord_geocode):
        mock_coord_geocode.return_value = "geocoded_location"

        test_record = self.stub_station_record(
            station_id_field="001",
            station_postcode_field="postcode",
            station_easting_field="530264",
            station_northing_field="179650",
            station_uprn_field="uprn",
        )
        location, location_source = self.importer.get_station_point(test_record)
        mock_coord_geocode.assert_called_once_with(test_record)
        self.assertEqual(location, mock_coord_geocode.return_value)
        self.assertEqual(location_source, LocationSourceChoices.COORDINATES)

    @patch(
        "data_importers.base_importers.BaseCsvStationsCsvAddressesImporter.geocode_from_uprn",
    )
    def test_get_station_point_with_uprn(self, mock_uprn_geocode):
        mock_uprn_geocode.return_value = "geocoded_location"

        test_record = self.stub_station_record(
            station_id_field="001",
            station_postcode_field="postcode",
            station_easting_field="0",
            station_northing_field="0",
            station_uprn_field="uprn",
        )
        location, location_source = self.importer.get_station_point(test_record)
        mock_uprn_geocode.assert_called_once_with(test_record)
        self.assertEqual(location, mock_uprn_geocode.return_value)
        self.assertEqual(location_source, LocationSourceChoices.UPRN)
