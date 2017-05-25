from django.contrib.gis.geos import Point
from django.db import connection
from pollingstations.models import PollingDistrict
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter
from data_finder.helpers import geocode_point_only, PostcodeError


class Command(BaseShpStationsShpDistrictsImporter):
    council_id       = 'E08000033'
    districts_name   = 'parl.2017-06-08/Version 1/polling_districts.shp'
    stations_name    = 'parl.2017-06-08/Version 1/polling_districts.shp'
    elections        = ['parl.2017-06-08']

    def district_record_to_dict(self, record):
        # exclude duplicate/ambiguous code
        if str(record[1]).strip() == 'DC':
            return None

        return {
            'internal_council_id': str(record[1]).strip(),
            'name': str(record[0]).strip(),
        }

    def station_record_to_dict(self, record):
        # exclude duplicate/ambiguous code
        if str(record[1]).strip() == 'DC':
            return None

        # grab the last bit of the address - it might be a postcode
        postcode = record[2].split(",")[-1].strip()

        # attempt to derive a point from it
        try:
            point = geocode_point_only(postcode)
            location = Point(point['wgs84_lon'], point['wgs84_lat'], srid=4326)
        except PostcodeError:
            location = None

        return {
            'location': location,
            'internal_council_id': str(record[1]).strip(),
            'address': str(record[2]).strip(),
            'postcode': '',
            'polling_district_id': str(record[1]).strip(),
        }

    def post_import(self):
        # fix dodgy polygons
        print("running fixup SQL")
        table_name = PollingDistrict()._meta.db_table

        cursor = connection.cursor()
        cursor.execute("""
        UPDATE {0}
         SET area=ST_Multi(ST_CollectionExtract(ST_MakeValid(area), 3))
         WHERE NOT ST_IsValid(area);
        """.format(table_name))
