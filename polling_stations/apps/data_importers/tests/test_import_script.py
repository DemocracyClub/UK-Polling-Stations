from django.test import TestCase

from data_importers.import_script import ImportScript


class ImportScriptTest(TestCase):
    def test_xpress(self):
        test_import_script = ImportScript(
            **{
                "council_id": "AAA",
                "ems": "Idox Eros (Halarose)",
                "addresses_name": "path/to/file.csv",
                "stations_name": "path/to/file.csv",
                "encoding": "utf-8",
                "elections": [],
            }
        )

        self.assertEqual(
            test_import_script.script,
            """from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "AAA"
    addresses_name = "path/to/file.csv"
    stations_name = "path/to/file.csv"
    elections = []
""",
        )

    def test_encoding(self):
        test_import_script = ImportScript(
            **{
                "council_id": "AAA",
                "ems": "Idox Eros (Halarose)",
                "addresses_name": "path/to/file.csv",
                "stations_name": "path/to/file.csv",
                "encoding": "windows-1252",
                "elections": [],
            }
        )

        self.assertEqual(
            test_import_script.script,
            """from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "AAA"
    addresses_name = "path/to/file.csv"
    stations_name = "path/to/file.csv"
    elections = []
    csv_encoding = "windows-1252"
""",
        )

    def test_dc_tsv(self):
        test_import_script = ImportScript(
            **{
                "council_id": "AAA",
                "ems": "Democracy Counts",
                "addresses_name": "path/to/districts.tsv",
                "stations_name": "path/to/stations.tsv",
                "encoding": "utf-8",
                "elections": [],
            }
        )

        self.assertEqual(
            test_import_script.script,
            """from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "AAA"
    addresses_name = "path/to/districts.tsv"
    stations_name = "path/to/stations.tsv"
    elections = []
    csv_delimiter = "\\t"
""",
        )
