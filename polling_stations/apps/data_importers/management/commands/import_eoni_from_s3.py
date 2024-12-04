import csv
import re
from pathlib import Path

import chardet
import sentry_sdk
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pyproj import Transformer

from data_importers.s3wrapper import parse_s3_uri, S3Wrapper
from data_importers.management.commands.import_eoni import Command as EONI_Importer

from polling_stations.settings.constants.importers import EONIImportScheme


def attempt_decode(body: bytes):
    sample = get_body_sample(body)
    detection = chardet.detect(sample)
    encoding = detection["encoding"]
    if encoding == "utf-16le":
        return body.decode(encoding), encoding
    encodings = ["utf-8", "windows-1252", "latin-1"]
    for encoding in encodings:
        try:
            return body.decode(encoding), encoding
        except UnicodeDecodeError as e:
            last_exception = e
            continue
    raise last_exception


def get_body_sample(body: bytes):
    if b"\r\n" in body:
        line_sep = b"\r\n"
    elif b"\n" in body:
        line_sep = b"\n"
    else:
        return body
    lines = body.split(line_sep)
    if len(lines) > 20:
        return line_sep.join(lines[:20])
    return line_sep.join(lines)


def is_eoni_export_key(key: str) -> bool:
    """
    Should return true for things like:
    '2023-04-12-EONIextract.txt',
    '2024-07-03-EONIextract-sample.txt',
    '2024-11-21-EONIextract_NEW.txt'

    """
    eoni_export_key_pattern = re.compile(
        r"""
        ^           # Start of string
        20[2-9]     # First 3 digits of year: 202-209
        [0-9]       # Last digit of year: 0-9
        -           # Separator
        [0-9]{2}    # Month as 2 digits
        -           # Separator
        [0-9]{2}    # Day as 2 digits
        -.+         # Hyphen followed by any text
        \.txt       # Literal .txt extension
        """,
        re.VERBOSE,
    )
    if eoni_export_key_pattern.match(key):
        return True
    return False


class EONIUploadValidationError(Exception):
    pass


class Command(BaseCommand):
    help = (
        "Downloads EONI data from S3 and:"
        "\n  - reprojects coordinates from EPSG:29902 to EPSG:4326"
        "\n  - controls the eoni election scheme that is imported"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dc_environment = None
        self.output_path = None
        self.address_non_coord_fields = [
            "PRO_ID",
            "PRO_LINE1",
            "PRO_LINE2",
            "PRO_LINE3",
            "PRO_LINE4",
            "PRO_LINE5",
            "PRO_POSTCODE",
            "PRO_FULLADDRESS",
            "PRO_UPRN",
        ]
        self.address_x_field = "PRO_X_COR"
        self.address_y_field = "PRO_Y_COR"
        self.national_suffix = "_WM"
        self.local_suffix = "_LC"
        self.station_non_coord_fields = [
            "PREM_ID",
            "PREM_NAME",
            "PREM_LINE1",
            "PREM_LINE2",
            "PREM_LINE3",
            "PREM_LINE4",
            "PREM_LINE5",
            "PREM_POSTCODE",
            "PREM_FULLADDRESS",
            "PREM_UPRN",
        ]
        self.station_x_field_prefix = "PREM_X_COR"
        self.station_y_field_prefix = "PREM_Y_COR"

        self.national_station_fields = [
            field + self.national_suffix
            for field in self.station_non_coord_fields
            + [f"{self.station_x_field_prefix}", f"{self.station_y_field_prefix}"]
        ]
        self.local_station_fields = [
            field + self.local_suffix
            for field in self.station_non_coord_fields
            + [f"{self.station_x_field_prefix}", f"{self.station_y_field_prefix}"]
        ]
        self.header = (
            self.address_non_coord_fields
            + [self.address_x_field, self.address_y_field]
            + self.national_station_fields
            + self.local_station_fields
        )
        self.import_scheme = None
        self.local_path = None
        self.bucket_name = None
        self.input_key = None
        self.s3_wrapper = None

    def add_arguments(self, parser):
        parser.add_argument(
            "--import-scheme",
            help="The EONI election scheme you want to import",
            default=settings.EONI_IMPORT_SCHEME,
            choices=EONIImportScheme.values,
        )
        parser.add_argument(
            "--input-uri",
            help="Optional S3 URI in the format s3://bucket_name/key",
            default=None,
        )
        parser.add_argument(
            "--output",
            help='Output file path. If not provided, will use "eoni_reprojected.csv" in current directory',
            default="eoni_reprojected.csv",
        )
        parser.add_argument(
            "--keep-temp-files",
            action="store_true",
            help="Do not delete temporary files after processing",
        )
        parser.add_argument(
            "--send-slack-report",
            action="store_true",
            help="Ask import_eoni command to report to slack",
        )

    def handle(self, *args, **options):
        try:
            # Set env.
            # Command works without, but requires '--input-uri' and will only post to test channel in slack.
            self.dc_environment = settings.DC_ENVIRONMENT

            # Set up s3 config
            self.set_s3_key_and_wrapper(options)

            # Download file from s3
            self.download_file()

            # Decode file
            self.decode_csv()

            # Validate file
            self.validate_file()

            # Set import scheme
            self.set_import_scheme(options)

            # Set outpath for reprojected file
            self.set_output_path(options)

            # Create reprojected file at output path
            self.create_reprojected_file()

            # Run the import
            self.call_import_eoni_command(options)

        finally:
            # Cleanup
            self.cleanup(options)

    def set_s3_key_and_wrapper(self, options):
        # Set bucket_name  based on input method
        if options.get("input_uri"):
            self.stdout.write("Setting s3 config from input_uri")
            bucket_name, input_key = parse_s3_uri(options["input_uri"])
            self.bucket_name = bucket_name
            self.input_key = input_key
            self.s3_wrapper = S3Wrapper(bucket_name=self.bucket_name)

            return

        # If no input URI is provided, require DC_ENVIRONMENT for default bucket_name
        if not self.dc_environment:
            raise CommandError(
                "Either --input-uri or DC_ENVIRONMENT environment variable must be set"
            )
        self.stdout.write(
            "Inferring s3 config from DC_ENVIRONMENT environment variable"
        )
        self.stdout.write(f"DC_ENVIRONMENT: {self.dc_environment}")

        self.bucket_name = f"eoni-data.wheredoivote.co.uk.{self.dc_environment}"
        self.s3_wrapper = S3Wrapper(bucket_name=self.bucket_name)

        self.input_key = self.get_latest_file_on_s3()

    def download_file(self):
        self.stdout.write(
            f"Fetching latest file:\n\ts3://{self.bucket_name}/{self.input_key}"
        )
        self.local_path, downloaded = self.s3_wrapper.download_file(self.input_key)
        if downloaded:
            self.stdout.write(f"Downloaded and saved to:\n\t{self.local_path}")
        else:
            self.stdout.write(f"Using cached version found at:\n\t{self.local_path}")

    def get_latest_file_on_s3(self):
        objects = self.s3_wrapper.bucket.objects.all()
        object_keys = sorted(
            [obj.key for obj in objects if is_eoni_export_key(obj.key)]
        )

        if len(object_keys) == 0:
            raise CommandError(
                f"Failed to find any EONI export keys for {self.bucket_name}"
            )
        return object_keys[-1]

    def decode_csv(self):
        with open(self.local_path, "rb") as csv_file:
            body = csv_file.read()
            try:
                decoded, csv_encoding = attempt_decode(body)
                csv_encoding = csv_encoding
            except UnicodeDecodeError:
                raise CommandError("Failed to decode CSV using any expected encoding")
            self.stdout.write(f"{csv_encoding} encoding detected.")
            self.reader = csv.DictReader(decoded.splitlines())

    def validate_file(self):
        fieldnames = self.reader.fieldnames
        header_issues = []
        extra_fields = [field for field in fieldnames if field not in self.header]
        missing_fields = [field for field in self.header if field not in fieldnames]

        if extra_fields:
            header_issues.append(
                f"CSV has following extra fields: {', '.join(extra_fields)}"
            )

        if missing_fields:
            header_issues.append(f"CSV has missing fields: {', '.join(missing_fields)}")

        if header_issues:
            sentry_sdk.set_context(
                "Command",
                {
                    "file": f"s3://{self.bucket_name}/{self.input_key}",
                    "error": "CSV validation error",
                    "issues": header_issues,
                },
            )
            self.stderr.write(
                "Found issues with header."
                f"Expected header: {self.header}"
                f"File header: {fieldnames}"
            )
            self.stderr.write("\n".join(header_issues))
            raise CommandError("Failed to validate CSV")

        self.stdout.write("CSV valid")

    def set_import_scheme(self, options):
        try:
            self.import_scheme = options["import_scheme"]
            self.stdout.write(f"Using {self.import_scheme} import scheme.")
        except KeyError:
            raise CommandError(
                "No import scheme specified. "
                "This probably means the constant in constants/importers.py hasn't been set."
            )

    def set_output_path(self, options):
        output_path = Path(options["output"])
        if output_path.exists():
            self.stdout.write(
                f"Deleting existing file found at:\n\t{output_path.resolve()}"
            )
            output_path.unlink()

        self.output_path = str(output_path.resolve())

        self.stdout.write(
            f"Writing output for import_eoni command to:\n\t{self.output_path}"
        )

    def reproject_coord(self, x, y, transformer, row_id):
        try:
            return transformer.transform(x, y)
        except TypeError as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Warning: Failed to transform coords in {row_id} "
                    f"{x =}"
                    f"{y =}"
                )
            )
            self.stdout.write(self.style.WARNNG(f"Exception was: {str(e)}"))
            return None, None

    def reproject_row(self, row, scheme_suffix, transformer, row_num):
        station_x_coord_field = f"{self.station_x_field_prefix}{scheme_suffix}"
        station_y_coord_field = f"{self.station_y_field_prefix}{scheme_suffix}"
        new_row = {field: row[field] for field in self.address_non_coord_fields}
        address_lon, address_lat = self.reproject_coord(
            row[self.address_x_field],
            row[self.address_y_field],
            transformer,
            row_num,
        )

        station_lon, station_lat = self.reproject_coord(
            row[station_x_coord_field],
            row[station_y_coord_field],
            transformer,
            row_num,
        )

        if not all((address_lon, address_lat, station_lon, station_lat)):
            return None

        new_row[self.address_x_field.replace("COR", "4326")] = address_lon
        new_row[self.address_y_field.replace("COR", "4326")] = address_lat

        new_row.update(
            {
                field: row[f"{field}{scheme_suffix}"]
                for field in self.station_non_coord_fields
            }
        )
        new_row[self.station_x_field_prefix.replace("COR", "4326")] = station_lon
        new_row[self.station_y_field_prefix.replace("COR", "4326")] = station_lat
        return new_row

    def create_reprojected_file(self):
        scheme_suffix = self.national_suffix

        if self.import_scheme == "LOCAL":
            scheme_suffix = self.local_suffix

        transformer = Transformer.from_crs("epsg:29902", "epsg:4326", always_xy=True)

        new_rows = []
        failed_rows = []

        row_count = 0
        for row_num, row in enumerate(self.reader, 1):
            row_count += 1
            new_row = self.reproject_row(row, scheme_suffix, transformer, row_count)
            if new_row:
                new_rows.append(new_row)
            else:
                failed_rows.append(row_count)

        with open(self.output_path, mode="w", newline="") as csv_file:
            fieldnames = new_rows[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created reprojected file with {len(new_rows)} rows"
            )
        )
        if len(failed_rows) > 0:
            sentry_sdk.set_context(
                "Command",
                {
                    "file": f"s3://{self.bucket_name}/{self.input_key}",
                    "error": "Reprojection error",
                    "issues": [
                        f"Failed to reproject {len(failed_rows)} rows: {failed_rows}"
                    ],
                },
            )
            raise CommandError("Failed to reproject all rows")

    def call_import_eoni_command(self, options):
        eoni_importer = EONI_Importer()

        importer_opts = {
            "cleanup": True,
            "reprojected": True,
            "eoni_csv": self.output_path,
            "verbosity": 1,
            "include_past_elections": True,
        }

        if options.get("send_slack_report"):
            if self.dc_environment == "production":
                channel = settings.BOTS_CHANNEL
            else:
                channel = settings.BOT_TESTING_CHANNEL

            importer_opts["slack"] = channel

        eoni_importer.handle(**importer_opts)

    def cleanup(self, options):
        if options.get("keep_temp_files"):
            self.stdout.write(f"Temporary file at {self.output_path} not deleted.")
            return

        if self.output_path:
            Path(self.output_path).unlink(missing_ok=True)
            self.stdout.write(f"Temporary file at {self.output_path} deleted.")
