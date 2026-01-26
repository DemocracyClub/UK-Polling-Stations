import datetime
import textwrap

from councils.tests.factories import CouncilFactory
from django.test import TestCase
from django.utils import timezone
from file_uploads.tests.factories import FileFactory, UploadFactory


class UploadManagerWithStatus(TestCase):
    election_date = timezone.now().date() + datetime.timedelta(weeks=4)
    last_week = timezone.now().date() - datetime.timedelta(weeks=1)

    def test_import_script_ok(self):
        upload = UploadFactory(
            election_date=self.election_date,
            timestamp=self.last_week,
            gss=CouncilFactory(council_id="FOO"),
        )
        FileFactory(
            upload_id=upload.id,
            csv_rows=132764,
            key="FOO/xyx/data.csv",
            ems="Xpress DC",
        )
        self.assertEqual(
            upload.import_script,
            textwrap.dedent(
                f"""\
            from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


            class Command(BaseXpressDemocracyClubCsvImporter):
                council_id = "FOO"
                addresses_name = "xyx/data.csv"
                stations_name = "xyx/data.csv"
                elections = ["{self.election_date.strftime('%Y-%m-%d')}"]
                csv_encoding = ""
                """
            ),
        )

    def test_import_script_ok_two_files(self):
        upload = UploadFactory(
            election_date=self.election_date,
            timestamp=self.last_week,
            gss=CouncilFactory(council_id="FOO"),
        )
        FileFactory(
            upload_id=upload.id,
            csv_rows=132764,
            key="FOO/xyx/data_districts.csv",
            ems="Democracy Counts",
        )
        FileFactory(
            upload_id=upload.id,
            csv_rows=120,
            key="FOO/xyx/data_stations.csv",
            ems="Democracy Counts",
        )

        self.assertEqual(
            upload.import_script,
            textwrap.dedent(
                f"""\
            from data_importers.management.commands import BaseDemocracyCountsCsvImporter


            class Command(BaseDemocracyCountsCsvImporter):
                council_id = "FOO"
                addresses_name = "xyx/data_districts.csv"
                stations_name = "xyx/data_stations.csv"
                elections = ["{self.election_date.strftime('%Y-%m-%d')}"]
                csv_encoding = ""
                """
            ),
        )

    def test_import_script_one_invalid_two_files(self):
        upload = UploadFactory(
            election_date=self.election_date,
            timestamp=self.last_week,
            gss=CouncilFactory(council_id="FOO"),
        )
        FileFactory(
            upload_id=upload.id,
            csv_rows=132764,
            key="FOO/xyx/data_districts.csv",
            ems="Democracy Counts",
            csv_valid=False,
        )
        FileFactory(
            upload_id=upload.id,
            csv_rows=120,
            key="FOO/xyx/data_stations.csv",
            ems="Democracy Counts",
        )

        with self.assertRaises(Exception):
            upload.import_script

    def test_import_script_two_invalid_two_files(self):
        upload = UploadFactory(
            election_date=self.election_date,
            timestamp=self.last_week,
            gss=CouncilFactory(council_id="FOO"),
        )
        FileFactory(
            upload_id=upload.id,
            csv_rows=132764,
            key="FOO/xyx/data_districts.csv",
            ems="Democracy Counts",
            csv_valid=False,
        )
        FileFactory(
            upload_id=upload.id,
            csv_rows=120,
            key="FOO/xyx/data_stations.csv",
            ems="Democracy Counts",
            csv_valid=False,
        )

        with self.assertRaises(Exception):
            upload.import_script

    def test_import_script_no_files(self):
        upload = UploadFactory(
            election_date=self.election_date,
            timestamp=self.last_week,
            gss=CouncilFactory(council_id="FOO"),
        )

        with self.assertRaises(Exception):
            upload.import_script
