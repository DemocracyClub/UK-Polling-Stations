import os
import glob

from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'cleaned_ab_path',
            help='The path to the cleaned AddressBase file'
        )


    def handle(self, *args, **kwargs):
        glob_str = os.path.join(
            kwargs['cleaned_ab_path'],
            "*_cleaned.csv"
        )
        for cleaned_file_path in glob.glob(glob_str):
            print(cleaned_file_path)
            cursor = connection.cursor()

            cursor.execute("""
                COPY addressbase_address (UPRN,address,postcode,location)
                FROM '{}' (FORMAT CSV, DELIMITER ',', quote '"');
            """.format(cleaned_file_path))
