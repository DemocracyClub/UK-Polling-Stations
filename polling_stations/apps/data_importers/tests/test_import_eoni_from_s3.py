import csv
import os
import shutil
from pathlib import Path
from unittest.mock import patch

import boto3
import pytest
from moto import mock_aws

from data_importers.management.commands.import_eoni_from_s3 import (
    Command,
    is_eoni_export_key,
)

# A minimal CSV row using the current EONI header format.
# Coordinates are in Irish Grid (EPSG:29902), roughly central Belfast.
EONI_CSV_ROW = {
    "PRO_ID": "1",
    "PRO_LINE1": "42",
    "PRO_LINE2": "TEST STREET",
    "PRO_LINE3": "",
    "PRO_LINE4": "BELFAST",
    "PRO_LINE5": "",
    "PRO_POSTCODE": "BT99 9AA",
    "PRO_FULLADDRESS": "42 TEST STREET, BELFAST, BT99 9AA",
    "PRO_UPRN": "99999999999",
    "PRO_X_COR": "340700",
    "PRO_Y_COR": "373800",
    "PREM_ID_WM": "111",
    "PREM_NAME_WM": "PUBLIC BUILDING",
    "PREM_LINE1_WM": "THE SQUARE",
    "PREM_LINE2_WM": "",
    "PREM_LINE3_WM": "",
    "PREM_LINE4_WM": "BELFAST",
    "PREM_LINE5_WM": "",
    "PREM_POSTCODE_WM": "BT99 9BB",
    "PREM_FULLADDRESS_WM": "PUBLIC BUILDING, THE SQUARE, BELFAST, BT99 9BB",
    "PREM_UPRN_WM": "8888888888",
    "PREM_FILL_COLOUR_WM": "#DDFF00",
    "PREM_BORDER_COLOUR_WM": "#ffffff",
    "PREM_X_COR_WM": "340500",
    "PREM_Y_COR_WM": "373500",
    "PREM_ID_LC": "222",
    "PREM_NAME_LC": "PUBLIC BUILDING",
    "PREM_LINE1_LC": "THE SQUARE",
    "PREM_LINE2_LC": "",
    "PREM_LINE3_LC": "",
    "PREM_LINE4_LC": "BELFAST",
    "PREM_LINE5_LC": "",
    "PREM_POSTCODE_LC": "BT99 9BB",
    "PREM_FULLADDRESS_LC": "PUBLIC BUILDING, THE SQUARE, BELFAST, BT99 9BB",
    "PREM_UPRN_LC": "8888888888",
    "PREM_FILL_COLOUR_LC": "#DDFF00",
    "PREM_BORDER_COLOUR_LC": "#ffffff",
    "PREM_X_COR_LC": "340500",
    "PREM_Y_COR_LC": "373500",
}

BUCKET_NAME = "test-eoni-bucket"
S3_KEY = "2026-04-01-EONIextract.txt"
S3_CACHE_DIR = Path("s3cache") / BUCKET_NAME


def build_eoni_csv_bytes():
    """Build a CSV bytestring matching the current EONI header format."""
    import io

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=EONI_CSV_ROW.keys())
    writer.writeheader()
    writer.writerow(EONI_CSV_ROW)
    return buf.getvalue().encode("utf-8")


class TestIsEoniExportKey:
    def test_standard_key(self):
        assert is_eoni_export_key("2026-04-01-EONIextract.txt") is True

    def test_key_with_suffix(self):
        assert is_eoni_export_key("2024-11-21-EONIextract_NEW.txt") is True

    def test_non_matching_key(self):
        assert is_eoni_export_key("readme.txt") is False


class TestImportEoniFromS3:
    """
    Smoke test: download from mocked S3, validate the new header format,
    reproject coordinates, and verify the output CSV is correct.

    The final call_import_eoni_command step is patched out because it
    requires a fully populated database with NI council geometries.
    """

    def setup_method(self):
        # Prevent real AWS credentials from leaking into moto tests
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"

        self.s3mock = mock_aws()
        self.s3mock.start()

        conn = boto3.client("s3")
        conn.create_bucket(Bucket=BUCKET_NAME)
        conn.put_object(
            Bucket=BUCKET_NAME,
            Key=S3_KEY,
            Body=build_eoni_csv_bytes(),
        )

    def teardown_method(self):
        self.s3mock.stop()
        # S3Wrapper caches downloads locally; clean up after each test
        if S3_CACHE_DIR.exists():
            shutil.rmtree(S3_CACHE_DIR)

    @patch.object(Command, "call_import_eoni_command")
    def test_download_validate_and_reproject(self, mock_import, tmp_path, settings):
        settings.DC_ENVIRONMENT = None

        output_path = str(tmp_path / "reprojected.csv")

        cmd = Command()
        cmd.handle(
            input_uri=f"s3://{BUCKET_NAME}/{S3_KEY}",
            output=output_path,
            import_scheme="NATIONAL",
            keep_temp_files=True,
            send_slack_report=False,
        )

        # The import_eoni command should have been called once
        mock_import.assert_called_once()

        # Verify the reprojected output file exists and has expected content
        assert Path(output_path).exists()

        with open(output_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 1

        # Address fields are preserved (without suffix)
        assert rows[0]["PRO_POSTCODE"] == "BT99 9AA"
        assert rows[0]["PRO_UPRN"] == "99999999999"

        # Station fields come from the _WM (national) scheme, without suffix
        assert rows[0]["PREM_ID"] == "111"
        assert rows[0]["PREM_NAME"] == "PUBLIC BUILDING"
        assert rows[0]["PREM_POSTCODE"] == "BT99 9BB"

        # Colour fields are carried through
        assert rows[0]["PREM_FILL_COLOUR"] == "#DDFF00"
        assert rows[0]["PREM_BORDER_COLOUR"] == "#ffffff"

        # Coordinates have been reprojected from Irish Grid to WGS84
        assert float(rows[0]["PRO_X_4326"]) == pytest.approx(-5.824, abs=0.001)
        assert float(rows[0]["PRO_Y_4326"]) == pytest.approx(54.593, abs=0.001)
        assert float(rows[0]["PREM_X_4326"]) == pytest.approx(-5.827, abs=0.001)
        assert float(rows[0]["PREM_Y_4326"]) == pytest.approx(54.590, abs=0.001)

    @patch.object(Command, "call_import_eoni_command")
    def test_local_scheme_uses_lc_fields(self, mock_import, tmp_path, settings):
        settings.DC_ENVIRONMENT = None

        output_path = str(tmp_path / "reprojected.csv")

        cmd = Command()
        cmd.handle(
            input_uri=f"s3://{BUCKET_NAME}/{S3_KEY}",
            output=output_path,
            import_scheme="LOCAL",
            keep_temp_files=True,
            send_slack_report=False,
        )

        with open(output_path) as f:
            rows = list(csv.DictReader(f))

        # Station fields should come from the _LC scheme
        assert rows[0]["PREM_ID"] == "222"
        assert rows[0]["PREM_NAME"] == "PUBLIC BUILDING"
        assert rows[0]["PREM_FILL_COLOUR"] == "#DDFF00"
