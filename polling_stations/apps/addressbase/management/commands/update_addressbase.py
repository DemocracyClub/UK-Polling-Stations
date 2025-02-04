import tempfile
from pathlib import Path

import boto3
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from uk_geo_utils.base_importer import BaseImporter

from councils.models import Council
from data_importers.event_helpers import record_teardown_event
from data_importers.models import DataQuality
from polling_stations.db_routers import get_principal_db_name
from pollingstations.models import PollingDistrict, PollingStation, AdvanceVotingStation

PRINCIPAL_DB_NAME = get_principal_db_name()


def get_file_from_s3(uri):
    if not uri.startswith("s3://"):
        raise Exception("url must start with s3://")
    if not uri.lower().endswith(".csv"):
        raise Exception("url must end with .csv")
    bucket = uri.split("/")[2]
    key = "/".join(uri.split("/")[3:])
    tmp = tempfile.NamedTemporaryFile(delete=False)
    bucket = boto3.resource("s3").Bucket(bucket)
    bucket.download_file(key, tmp.name)
    return tmp.name


class AddressbaseUpdater(BaseImporter):
    def get_table_name(self):
        return "addressbase_address"

    def import_data_to_temp_table(self):
        copy_string = f"""
        COPY {self.temp_table_name} (UPRN, address, postcode, location, addressbase_postal)
        FROM STDIN
        WITH (FORMAT CSV, DELIMITER ',', QUOTE '"');
        """
        self.stdout.write(f"Executing: {copy_string}")
        with open(self.data_path) as f:
            self.cursor.copy_expert(copy_string, f)


class UprnToCouncilUpdater(BaseImporter):
    def get_table_name(self):
        return "addressbase_uprntocouncil"

    def import_data_to_temp_table(self):
        copy_string = f"""
        COPY {self.temp_table_name} (uprn, lad, polling_station_id, advance_voting_station_id)
        FROM STDIN
        WITH (FORMAT CSV, DELIMITER ',', null '\\N');
        """
        self.stdout.write(f"Executing: {copy_string}")
        with open(self.data_path) as f:
            self.cursor.copy_expert(copy_string, f)


class Command(BaseCommand):
    """
    Usage:

    ./manage.py update_addressbase \
        --addressbase-s3-uri='s3://bucket/addressbase/sample/addressbase_cleaned/addressbase_cleaned.csv' \
        --uprntocouncil-s3-uri='s3://bucket/addressbase/sample/uprn-to-council/uprn-to-councils.csv'
    or
     ./manage.py update_addressbase \
        --addressbase-path /path/to/addressbase_cleaned.csv \
        --uprntocouncil-path /path/to/uprn-to-councils.csv

    """

    help = (
        "Updates both Addressbase and UPRN to Council mapping tables from local files"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean_up_uprntocouncil_file = False
        self.clean_up_addressbase_file = False

    def add_arguments(self, parser):
        addressbase_group = parser.add_mutually_exclusive_group(required=True)
        addressbase_group.add_argument(
            "--addressbase-path",
            help="Local path to the Addressbase data file",
        )
        addressbase_group.add_argument(
            "--addressbase-s3-uri",
            help="S3 URI for Addressbase data file",
        )
        uprntocouncil_group = parser.add_mutually_exclusive_group(required=True)
        uprntocouncil_group.add_argument(
            "--uprntocouncil-path",
            help="Local path to the UPRN to Council data file",
        )
        uprntocouncil_group.add_argument(
            "--uprntocouncil-s3-uri",
            help="S3 URI for UPRN to Council data file",
        )
        parser.add_argument(
            "--database",
            default=PRINCIPAL_DB_NAME,
            help="Database name. Defaults to PRINCIPAL_DB_NAME - i.e. RDS if you're on EC2",
        )

    def teardown(self):
        self.stdout.write(
            "New addresses imported. Deleting all Polling Stations, Advance Polling Stations and Polling Districts..."
        )
        for council in Council.objects.with_polling_stations_in_db():
            record_teardown_event(council.council_id)
            PollingDistrict.objects.all().delete()
            PollingStation.objects.all().delete()
            AdvanceVotingStation.objects.all().delete()
            DataQuality.objects.all().update(
                report="", num_addresses=0, num_districts=0, num_stations=0
            )

        self.stdout.write("..deleted.")

    def handle(self, *args, **options):
        addressbase_path = options.get("addressbase_path", None)
        uprntocouncil_path = options.get("uprntocouncil_path", None)
        if options.get("addressbase_s3_uri"):
            addressbase_path = get_file_from_s3(options["addressbase_s3_uri"])
            self.clean_up_addressbase_file = True
        if options.get("uprntocouncil_s3_uri"):
            uprntocouncil_path = get_file_from_s3(options["uprntocouncil_s3_uri"])
            self.clean_up_uprntocouncil_file = True

        self.stdout.write(f"addressbase_path set to {addressbase_path}")
        self.stdout.write(f"uprntocouncil_path to {uprntocouncil_path}")

        database_name = options["database"]
        connection = connections[database_name]
        cursor = connection.cursor()

        # Create addressbase updater and set cursor
        addressbase_updater = AddressbaseUpdater()
        addressbase_updater.connection = connection
        addressbase_updater.cursor = cursor

        # Create addressbase updater and set cursor
        uprntocouncil_updater = UprnToCouncilUpdater()
        uprntocouncil_updater.connection = connection
        uprntocouncil_updater.cursor = cursor

        # Set the data_path on each updater instance
        addressbase_updater.data_path = addressbase_path
        uprntocouncil_updater.data_path = uprntocouncil_path

        # Get constraints and index information for both tables
        addressbase_updater.get_constraints_and_index_statements()
        uprntocouncil_updater.get_constraints_and_index_statements()

        try:
            # Create empty temp tables for both
            self.stdout.write("Creating temporary tables...")
            addressbase_updater.create_temp_table()
            uprntocouncil_updater.create_temp_table()

            # Import data into temp tables
            self.stdout.write("Importing data into temporary tables...")
            addressbase_updater.import_data_to_temp_table()
            uprntocouncil_updater.import_data_to_temp_table()

            # Add temp primary keys
            self.stdout.write("Adding primary keys to temporary tables...")
            addressbase_updater.add_temp_primary_key()
            uprntocouncil_updater.add_temp_primary_key()

            # Build temp indexes
            self.stdout.write("Building indexes on temporary tables...")
            addressbase_updater.build_temp_indexes()
            uprntocouncil_updater.build_temp_indexes()

            # Perform the table swaps in a single transaction
            with transaction.atomic(using=database_name):
                self.stdout.write("Starting atomic transaction for table swaps...")

                # Drop all foreign keys first
                if addressbase_updater.foreign_key_constraints:
                    addressbase_updater.drop_foreign_keys()
                if uprntocouncil_updater.foreign_key_constraints:
                    uprntocouncil_updater.drop_foreign_keys()

                # Rename old tables
                addressbase_updater.drop_old_table()
                uprntocouncil_updater.drop_old_table()

                # Rename temp tables
                addressbase_updater.rename_temp_table()
                uprntocouncil_updater.rename_temp_table()

                # Add foreign keys back
                if addressbase_updater.foreign_key_constraints:
                    addressbase_updater.add_foreign_keys()
                if uprntocouncil_updater.foreign_key_constraints:
                    uprntocouncil_updater.add_foreign_keys()
                self.teardown()
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully updated both Addressbase and UPRN to Council tables"
                )
            )

        finally:
            # Clean up both updaters
            self.stdout.write("Cleaning up...")
            addressbase_updater.db_cleanup()
            uprntocouncil_updater.db_cleanup()

            if self.clean_up_addressbase_file:
                Path(addressbase_path).unlink()
            if self.clean_up_uprntocouncil_file:
                Path(uprntocouncil_path).unlink()

            # We only need one report.
            addressbase_updater.report_on_replicaton_status()
