import datetime
from unittest.mock import patch

from addressbase.models import UprnToCouncil
from addressbase.tests.factories import UprnToCouncilFactory
from councils.models import Council
from councils.tests.factories import CouncilFactory
from data_importers.base_importers import BaseImporter
from django.core.management import CommandError
from django.test import TestCase
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
        self.base_importer_past_election = BaseImporter()
        self.base_importer_past_election.elections = ["2000-01-01"]
        self.base_importer_today_election = BaseImporter()
        self.base_importer_today_election.elections = [str(datetime.date.today())]
        self.base_importer_multi_election = BaseImporter()
        self.base_importer_multi_election.elections = [
            "2000-01-01",
            str(datetime.date.today()),
        ]
        self.base_importer_tomorrow_election = BaseImporter()
        self.base_importer_tomorrow_election.elections = [
            str(datetime.date.today() + datetime.timedelta(days=1))
        ]
        self.opts = {"nochecks": True, "verbosity": 0}

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

    def test_no_election_attribute(self):
        self.assertRaisesRegex(
            CommandError,
            r"Import script for .* does not have an elections attribute",
            self.base_importer.handle,
            self.council.council_id,
            **self.opts,
        )

    def test_election_in_past(self):
        self.assertRaisesRegex(
            CommandError,
            (
                r"'elections' attribute in the import script for .* only has dates in the past\n"
                r"self.elections=\['2000-01-01'\]Consider passing the '--include-past-elections' flag"
            ),
            self.base_importer_past_election.handle,
            self.council.council_id,
            **self.opts,
        )

    def test_covers_current_elections(self):
        self.assertFalse(self.base_importer.covers_current_elections())
        self.assertFalse(self.base_importer_past_election.covers_current_elections())
        self.assertTrue(self.base_importer_today_election.covers_current_elections())
        self.assertTrue(self.base_importer_multi_election.covers_current_elections())
        self.assertTrue(self.base_importer_tomorrow_election.covers_current_elections())
