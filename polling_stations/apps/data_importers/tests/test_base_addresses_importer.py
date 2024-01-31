from unittest.mock import patch

from councils.tests.factories import CouncilFactory
from data_importers.base_importers import BaseAddressesImporter
from django.test import TestCase
from file_uploads.tests.factories import FileFactory, UploadFactory


class MockLogger:
    logs = []

    def log_message(self, level, message, variable=None, pretty=False):
        self.logs.append(message)

    def clear_logs(self):
        self.logs = []


class BaseStationsImporterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.council = CouncilFactory(council_id="ABC")

    @patch(
        "data_importers.base_importers.BaseAddressesImporter.__abstractmethods__", set()
    )
    def setUp(self):
        self.base_addresses_importer = BaseAddressesImporter()
        self.base_addresses_importer.logger = MockLogger()
        FileFactory(
            upload=UploadFactory(gss=self.council),
            key="ABC/<date>/<timestamp>/polling_station_export.csv",
        )

    @patch("data_importers.base_importers.BaseAddressesImporter.council_id", "ABC")
    @patch(
        "data_importers.base_importers.BaseAddressesImporter.addresses_name",
        "<date>/<timestamp>/polling_station_export.csv",
    )
    def test_get_upload(self):
        self.assertTrue(self.base_addresses_importer.get_upload())
