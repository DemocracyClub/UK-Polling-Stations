from django.db import transaction
from django.db import connection
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter
from pollingstations.models import PollingDistrict

"""
Ashfield publish their data on data.gov.uk :D
..but they publish Excel and MapInfo binaries :(

I've converted these to CSV and SHP format
and uploaded that data to Amazon S3 for import purposes

Additionally there's a hashes only scraper at
https://morph.io/wdiv-scrapers/DC-PollingStations-Ashfield
polling the URLs to look for changes.
"""

class Command(BaseShpStationsShpDistrictsImporter):
    council_id = 'E07000170'
    srid = 27700
    districts_srid = 27700
    districts_name = 'New data/shp/polling_districts'
    stations_name = 'New data/shp/polling_stations.shp'
    elections = [
        'local.nottinghamshire.2017-05-04',
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[0]).strip(),
            'name': '%s - %s' % (str(record[1]).strip(), str(record[0]).strip()),
            'polling_station_id': str(record[3]).strip(),
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[0]).strip(),
            'address' : '%s\n%s' % (str(record[2]).strip(), str(record[3]).strip()),
            'postcode': str(record[4]).strip(),
        }

    @transaction.atomic
    def post_import(self):
        # fix self-intersecting polygon
        print("running fixup SQL")
        table_name = PollingDistrict()._meta.db_table

        cursor = connection.cursor()
        cursor.execute("""
        UPDATE {0}
         SET area=ST_Multi(ST_CollectionExtract(ST_MakeValid(area), 3))
         WHERE NOT ST_IsValid(area);
        """.format(table_name))
