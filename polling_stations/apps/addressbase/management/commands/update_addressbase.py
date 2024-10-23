from django.core.management.base import BaseCommand
from django.db import transaction
from uk_geo_utils.base_updater import BaseUpdater


class AddressbaseUpdater(BaseUpdater):
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


class UprnToCouncilUpdater(BaseUpdater):
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
    help = (
        "Updates both Addressbase and UPRN to Council mapping tables from local files"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--addressbase-path",
            required=True,
            help="Local path to the Addressbase data file",
        )
        parser.add_argument(
            "--uprntocouncil-path",
            required=True,
            help="Local path to the UPRN to Council data file",
        )

    def handle(self, *args, **options):
        addressbase_updater = AddressbaseUpdater()
        uprntocouncil_updater = UprnToCouncilUpdater()

        # Set the data_path on each updater instance
        addressbase_updater.data_path = options["addressbase_path"]
        uprntocouncil_updater.data_path = options["uprntocouncil_path"]

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
            with transaction.atomic():
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
