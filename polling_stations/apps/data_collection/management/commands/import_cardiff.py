"""
Import Cardiff
"""
from django.db import transaction
from django.db import connection

from data_collection.management.commands import BaseShpStationsShpDistrictsImporter
from pollingstations.models import PollingDistrict


class Command(BaseShpStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Braintree
    """
    council_id     = 'W06000015'
    districts_name = 'Polling Districts_region'
    stations_name  = 'Polling Stations_font_point.shp'
    elections      = [
        'local.cardiff.2017-05-04',
        'parl.2017-06-08'
    ]

    def parse_string(self, text):
        try:
            return text.strip().decode('latin-1')
        except AttributeError:
            return text.strip()

    def district_record_to_dict(self, record):
        code = self.parse_string(record[0])

        """
        Joe received following from Cardiff:

        Two polling districts SJ and QK
        The following streets are affected
          - SJ Duncan Close
          - QK Bethania Row
        but no updated data: exclude these 2 districts
        because we don't have the new boundaries
        """
        if code == 'SJ' or code == 'QK':
            return None

        return {
            'internal_council_id': code,
            'name': code
        }

    def station_record_to_dict(self, record):
        unique_id = "-".join(
                (self.parse_string(record[0]), self.parse_string(record[1]))
            ).strip()
        return {
            'internal_council_id': unique_id,
            'postcode'           : "",
            'address'            : self.parse_string(record[2]),
            'polling_district_id': self.parse_string(record[1]),
        }

    @transaction.atomic
    def post_import(self):
        """
        This data isn't great – the polygons seem to be corrupt in some way.

        PostGIS can fix them though!
        """
        print("running fixup SQL")
        table_name = PollingDistrict()._meta.db_table

        cursor = connection.cursor()
        cursor.execute("""
        UPDATE {0}
         SET area=ST_Multi(ST_CollectionExtract(ST_MakeValid(area), 3))
         WHERE NOT ST_IsValid(area);
        """.format(table_name))
        # Note the delibarate use of `.format` above – we don't want the table
        # names in quotes.  Use `%s` and a list as a 2nd arg to execute
        # if you're adding values at all.
