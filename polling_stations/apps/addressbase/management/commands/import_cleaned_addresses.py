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


    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        print("clearing existing data..")
        cursor.execute("TRUNCATE TABLE addressbase_address;")

        cleaned_file_path = os.path.abspath(os.path.join(
            kwargs['cleaned_ab_path'],
            "addressbase_cleaned.csv"
        ))

        print("importing from %s.." % (cleaned_file_path))

        cursor.execute("""
            COPY addressbase_address (UPRN,address,postcode,location)
            FROM '{}' (FORMAT CSV, DELIMITER ',', quote '"');
        """.format(cleaned_file_path))

        print("...done")
