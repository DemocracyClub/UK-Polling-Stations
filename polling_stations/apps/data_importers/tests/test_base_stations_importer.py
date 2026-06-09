import os
from unittest.mock import patch, Mock

from collections import namedtuple
from councils.tests.factories import CouncilFactory
from data_importers.base_importers import BaseStationsImporter
from data_importers.data_types import StationSet
from django.contrib.gis.geos import Point
from django.test import TestCase
from pollingstations.models import LocationSourceChoices


class MockLogger:
    logs = []

    def log_message(self, level, message, variable=None, pretty=False):
        self.logs.append(message)

    def clear_logs(self):
        self.logs = []


StubStationRecord = namedtuple(
    "StubStationRecord",
    [
        "station_id",
        "station_postcode",
        "station_easting",
        "station_northing",
        "station_uprn",
    ],
)


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


class BaseStationImporterGetStationPointTests(TestCase):
    @patch(
        "data_importers.base_importers.BaseStationsImporter.__abstractmethods__", set()
    )
    def setUp(self):
        self.importer = BaseStationsImporter()
        self.importer.logger = MockLogger()

        self.importer.allow_station_point_from_postcode = False

        self.test_record = StubStationRecord(
            station_id="test_id",
            station_postcode="AA1 1AA",
            station_easting="530264",
            station_northing="179650",
            station_uprn="123456789",
        )

        self.importer.get_station_id = Mock(return_value="test_id")

    @patch("data_importers.base_importers.BaseStationsImporter.get_station_coordinates")
    @patch(
        "data_importers.base_importers.BaseStationsImporter.geocode_from_coordinates"
    )
    def test_get_station_point_with_coordinates(
        self, mock_coord_geocode, mock_get_station_coordinates
    ):
        # We should prefer coordinates over other methods
        mock_coord_geocode.return_value = "geocoded_location"
        mock_get_station_coordinates.return_value = (
            self.test_record.station_easting,
            self.test_record.station_northing,
        )

        location, location_source = self.importer.get_station_point(self.test_record)
        mock_coord_geocode.assert_called_once_with(
            self.test_record.station_easting,
            self.test_record.station_northing,
        )
        self.assertEqual(location, mock_coord_geocode.return_value)
        self.assertEqual(location_source, LocationSourceChoices.COORDINATES)

    @patch("data_importers.base_importers.BaseStationsImporter.get_station_uprn")
    @patch("data_importers.base_importers.Address")
    def test_get_station_point_with_uprn(
        self,
        mock_address_model,
        mock_get_station_uprn,
    ):
        # We should prefer UPRN over postcode, but not coordinates
        self.test_record = self.test_record._replace(
            station_easting="",
            station_northing="",
        )
        mock_get_station_uprn.return_value = self.test_record.station_uprn
        return_value = "geocoded_location"
        mock_address_model.objects.get.return_value.location = return_value

        location, location_source = self.importer.get_station_point(self.test_record)
        mock_address_model.objects.get.assert_called_once_with(
            uprn=self.test_record.station_uprn
        )
        self.assertEqual(location, return_value)
        self.assertEqual(location_source, LocationSourceChoices.UPRN)

    @patch("data_importers.base_importers.BaseStationsImporter.get_station_postcode")
    @patch("data_importers.base_importers.BaseStationsImporter.geocode_from_postcode")
    def test_get_station_point_with_postcode(
        self, mock_postcode_geocode, mock_get_station_postcode
    ):
        # We should only attempt to geocode from postcode if allowed and we're missing coords/uprn
        self.importer.allow_station_point_from_postcode = True
        self.test_record = self.test_record._replace(
            station_easting="",
            station_northing="",
            station_uprn="",
        )
        mock_get_station_postcode.return_value = self.test_record.station_postcode
        mock_postcode_geocode.return_value = "geocoded_location"

        location, location_source = self.importer.get_station_point(self.test_record)
        mock_postcode_geocode.assert_called_once_with(self.test_record.station_postcode)
        self.assertEqual(location_source, LocationSourceChoices.POSTCODE)
        self.assertEqual(location, mock_postcode_geocode.return_value)

    def test_get_station_point_no_location_data(self):
        self.test_record = self.test_record._replace(
            station_postcode="",
            station_easting="",
            station_northing="",
            station_uprn="",
        )

        location, location_source = self.importer.get_station_point(self.test_record)
        self.assertEqual(location_source, LocationSourceChoices.NONE)
        self.assertIsNone(location)

    @patch("data_importers.base_importers.BaseStationsImporter.get_station_coordinates")
    @patch(
        "data_importers.base_importers.BaseStationsImporter.geocode_from_coordinates"
    )
    def test_get_station_point_invalid_coordinates(
        self, mock_coord_geocode, mock_get_station_coordinates
    ):
        test_cases = [
            ("27700", "-1", "179650"),  # Invalid easting
            ("27700", "530264", "-1"),  # Invalid northing
            ("27700", "700001", "179650"),  # Out of range easting
            ("27700", "530264", "1300001"),  # Out of range northing
            ("27700", "not_a_number", "179650"),  # Non-numeric easting
            ("27700", "530264", "not_a_number"),  # Non-numeric northing
            ("4326", "-91", "0"),  # Out of range latitude
            ("4326", "0", "181"),  # Out of range longitude
            ("4326", "not_a_number", "0"),  # Non-numeric latitude
            ("4326", "0", "not_a_number"),  # Non-numeric longitude
        ]

        for srid, x, y in test_cases:
            with self.subTest(srid=srid, x=x, y=y):
                self.importer.srid = srid
                self.test_record = self.test_record._replace(
                    station_postcode="",
                    station_easting=x,
                    station_northing=y,
                    station_uprn="",
                )
                mock_get_station_coordinates.return_value = (x, y)

                location, location_source = self.importer.get_station_point(
                    self.test_record
                )
                mock_coord_geocode.assert_not_called()
