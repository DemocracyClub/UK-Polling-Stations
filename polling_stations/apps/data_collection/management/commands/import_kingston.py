"""
Imports Kingston
"""
import sys

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseKamlImporter

class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from Kingston Council
    """
    council_id     = 'E09000021'
    districts_name = 'Polling_districts.kmz'
    stations_name  = 'Polling_stations.csv'

    csv_encoding   = 'latin-1'

    def station_record_to_dict(self, record):

        point = Point(float(record.eastings), float(record.northings), srid=self.get_srid())

        # split out address and postcode
        address = record.location
        address_parts = address.split(', ')
        postcode = address_parts[-1]
        del(address_parts[-1])
        address = "\n".join(address_parts)

        return {
            'internal_council_id': record.polling_station_address,
            'postcode':            postcode,
            'address':             address,
            'location':            point,
            'polling_district_id': record.polling_station_address
        }
