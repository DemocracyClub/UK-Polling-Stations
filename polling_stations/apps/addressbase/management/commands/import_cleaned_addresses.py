import os
import glob
from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'cleaned_ab_path',
            help='The path to the folder containing the cleaned AddressBase CSVs'
        )
        parser.add_argument(
            '-t',
            '--table',
            help='If you have extended the AbstractAddress model, use this flag to specify the table name for your child table',
            default='uk_geo_utils_address',
            required=False,
        )

    def handle(self, *args, **kwargs):
        self.table_name = kwargs['table']

        cursor = connection.cursor()
        print("clearing existing data..")
        cursor.execute("TRUNCATE TABLE %s;" % (self.table_name))

        cleaned_file_path = os.path.abspath(os.path.join(
            kwargs['cleaned_ab_path'],
            "addressbase_cleaned.csv"
        ))

        print("importing from %s.." % (cleaned_file_path))

        cursor.execute("""
            COPY {0} (UPRN,address,postcode,location)
            FROM '{1}' (FORMAT CSV, DELIMITER ',', quote '"');
        """.format(self.table_name, cleaned_file_path))

        print("...done")
