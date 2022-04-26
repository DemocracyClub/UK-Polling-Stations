import textwrap

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

    def test_update_existing_script(self):
        # The behavior we're looking for here:
        #
        # * the Command base class and import are changed according to ems
        # * the csv_encoding is added
        # * the csv_delimiter is removed
        # * addresses_name/stations_name/elections are updated
        # * we can handle addresses_name/stations_name being split over multiple lines
        # * trailing ClassDef content is commented out, but otherwise preserved verbatim
        # * content after the Command CLassDef is preserved verbatim

        test_import_script = ImportScript(
            **{
                "council_id": "AAA",
                "ems": "Democracy Counts",
                "addresses_name": "path/to/districts.csv",
                "stations_name": "path/to/stations.csv",
                "encoding": "windows-1252",
                "elections": ["2022-05-05"],
                "existing_script": textwrap.dedent(
                    """\
                    from data_importers.management.commands import BaseHalaroseCsvImporter

                    class Command(BaseHalaroseCsvImporter):
                        council_id = "AAA"
                        addresses_name = (
                            "old_path/to/districts.tsv"
                        )
                        stations_name = (
                            "old_path/to/stations.tsv"
                        )
                        elections = ["2021-05-06"]
                        csv_delimiter = "\\t"

                        def address_record_to_dict(self, record):
                            # Do something
                            return super().address_record_to_dict(record)

                    def something_after():
                        # comment
                        pass
                """
                ),
            }
        )

        self.assertEqual(
            test_import_script.script,
            textwrap.dedent(
                """\
                from data_importers.management.commands import BaseDemocracyCountsCsvImporter


                class Command(BaseDemocracyCountsCsvImporter):
                    council_id = "AAA"
                    addresses_name = "path/to/districts.csv"
                    stations_name = "path/to/stations.csv"
                    elections = ["2022-05-05"]
                    csv_encoding = "windows-1252"

                    # def address_record_to_dict(self, record):
                    #     # Do something
                    #     return super().address_record_to_dict(record)


                def something_after():
                    # comment
                    pass
                """
            ),
        )
