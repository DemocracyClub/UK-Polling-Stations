from uk_geo_utils.helpers import get_onsud_model
from uk_geo_utils.management.commands import import_cleaned_addresses
import os
from django.db import connection


class Command(import_cleaned_addresses.Command):
    def import_addressbase(self):
        self.onsud_table_name = get_onsud_model()._meta.db_table
        cleaned_file_path = os.path.abspath(
            os.path.join(self.path, "addressbase_cleaned.csv")
        )

        with open(cleaned_file_path, "r") as fp:
            cursor = connection.cursor()
            self.stdout.write(
                f"clearing existing {self.onsud_table_name} and {self.table_name} data.."
            )
            cursor.execute("TRUNCATE TABLE %s CASCADE;" % (self.table_name))

            self.stdout.write("importing from %s.." % (cleaned_file_path))
            cursor.copy_expert(
                """
                COPY %s (UPRN,address,postcode,location,addressbase_postal)
                FROM STDIN (FORMAT CSV, DELIMITER ',', quote '"');
            """
                % (self.table_name),
                fp,
            )

        self.stdout.write("...done")
