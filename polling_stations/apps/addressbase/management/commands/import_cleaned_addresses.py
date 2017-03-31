import os
import glob

from django.apps import apps
from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'addressbase' and 'pollingstations' apps
    """
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'cleaned_ab_path',
            help='The path to the folder containing the cleaned AddressBase CSVs'
        )


    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'addressbase' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check([
            apps.get_app_config('addressbase'),
            apps.get_app_config('pollingstations')
        ])

        glob_str = os.path.join(
            kwargs['cleaned_ab_path'],
            "*_cleaned.csv"
        )
        for cleaned_file_path in glob.glob(glob_str):
            cleaned_file_path = os.path.abspath(cleaned_file_path)
            print(cleaned_file_path)
            cursor = connection.cursor()

            cursor.execute("""
                COPY addressbase_address (UPRN,address,postcode,location)
                FROM '{}' (FORMAT CSV, DELIMITER ',', quote '"');
            """.format(cleaned_file_path))
