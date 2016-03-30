"""
Import Salford
"""
import sys
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Salford
    """
    council_id     = 'E08000006'
    districts_name = 'Salford_Polling_Districts'
    stations_name  = 'Polling_Stations.csv'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[0],
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)

        address_parts = [x.strip() for x in record.location.split(' ')]
        postcode = "%s %s" % (address_parts[-2], address_parts[-1])
        del(address_parts[-1])
        del(address_parts[-1])
        address = " ".join(address_parts)

        return {
            'internal_council_id': record.id,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location,
            'polling_district_id': record.polling_district_code
        }
