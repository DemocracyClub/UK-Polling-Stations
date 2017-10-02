import os
import glob
from django.db import connection
from django.core.management.base import BaseCommand
from uk_geo_utils.helpers import get_onsud_model


class Command(BaseCommand):
    """
    To import ONSUD, grab the latest release:
    http://ons.maps.arcgis.com/home/search.html?q=ONS%20Address%20Directory&t=content
    and run
    python manage.py import_onsud /path/to/data
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            help='Path to the directory containing the ONSUD CSVs'
        )

    def handle(self, *args, **kwargs):
        self.table_name = get_onsud_model()._meta.db_table

        cursor = connection.cursor()
        self.stdout.write("clearing existing data..")
        cursor.execute("TRUNCATE TABLE %s;" % (self.table_name))
        glob_str = os.path.join(kwargs['path'], "*.csv")
        self.stdout.write("importing from files..")
        for f in glob.glob(glob_str):
            self.stdout.write(f)
            fp = open(f, 'r')
            cursor.copy_expert("""
                COPY %s (
                uprn, ctry_flag, cty, lad, ward, hlthau, ctry,
                rgn, pcon, eer, ttwa, nuts, park, oa11, lsoa11, msoa11, parish,
                wz11, ccg, bua11, buasd11, ruc11, oac11, lep1, lep2, pfa, imd)
                FROM STDIN (FORMAT CSV, DELIMITER ',', QUOTE '"', HEADER);
            """ % (self.table_name), fp)
        self.stdout.write("...done")
