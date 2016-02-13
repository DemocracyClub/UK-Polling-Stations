"""
Import East Riding
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from East Riding of Yorkshire Council
    """
    council_id     = 'E06000011'
    districts_name = 'Polling_Districts.shpn'
    stations_name  = 'FOI6287_polling-stations.csv'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'name': record[2],
        }

    def station_record_to_dict(self, record):

        try:
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)
        addr = [record.name_of_station]
        addr += record.address.split(',')[:-1]
        return {
            'internal_council_id': record.code,
            'postcode'           : record.address.split(',')[-1],
            'address'            : "\n".join(addr),
            'location'           : location
        }
    
