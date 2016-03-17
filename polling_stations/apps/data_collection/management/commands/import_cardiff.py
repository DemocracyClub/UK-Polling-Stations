"""
Import Cardiff
"""
from django.db import transaction
from django.db import connection

from data_collection.management.commands import BaseShpShpImporter
from pollingstations.models import PollingDistrict


class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Braintree
    """
    council_id     = 'W06000015'
    districts_name = 'Polling Districts_region'
    stations_name  = 'Polling Stations_font_point.shp'
    elections      = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]

    def district_record_to_dict(self, record):
        if type(record[1]) == str:
            name = record[1]
        else:
            name = record[1].decode('latin-1')
        return {
            'internal_council_id': record[0].encode('utf8'),
            'name': name
        }

    def station_record_to_dict(self, record):
        unique_id = "-".join(
                (str(record[0]).strip('\'b'), str(record[1]).strip())
            ).strip()
        return {
            'internal_council_id': unique_id,
            'postcode'           : "",
            'address'            : str(record[2]),
            'polling_district_id': str(record[1]),
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
