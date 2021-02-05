from unittest.mock import patch

from django.test import TestCase

from addressbase.models import UprnToCouncil
from addressbase.tests.factories import UprnToCouncilFactory
from councils.models import Council
from councils.tests.factories import CouncilFactory
from data_importers.base_importers import BaseImporter
from pollingstations.tests.factories import PollingStationFactory


class BaseImporterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.council = CouncilFactory()
        cls.ps = PollingStationFactory()
        UprnToCouncilFactory(
            lad=cls.council.identifiers[0],
            polling_station_id=cls.ps.internal_council_id,
        )

    @patch("data_importers.base_importers.BaseImporter.__abstractmethods__", set())
    def setUp(self):
        self.base_importer = BaseImporter()

    def tearDown(self):
        pass

    def test_teardown(self):
        self.assertEqual(
            len(
                UprnToCouncil.objects.filter(
                    lad=self.council.identifiers[0],
                    polling_station_id=self.ps.internal_council_id,
                )
            ),
            1,
        )
        self.base_importer.teardown(self.council)
        self.assertEqual(
            len(
                UprnToCouncil.objects.filter(
                    lad=self.council.identifiers[0], polling_station_id=""
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                UprnToCouncil.objects.filter(
                    lad=self.council.identifiers[0],
                    polling_station_id=self.ps.internal_council_id,
                )
            ),
            0,
        )

    def test_get_council(self):
        council_from_reg = self.base_importer.get_council(self.council.council_id)
        self.assertIsInstance(council_from_reg, Council)
        self.assertRaises(
            Council.DoesNotExist,
            self.base_importer.get_council,
            council_id=self.council.identifiers[0],
        )
