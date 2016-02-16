"""
Import Brent
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter, import_polling_station_shapefiles


class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Brent Council
    """
    council_id     = 'E09000005'
    districts_name = 'polling_districts'
    stations_name  = 'polling_places.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[-1],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[2],
            'postcode'           : record[3].split(',')[-1],
            'address'            : record[3].decode('windows-1252')
        }
    
    
    def import_polling_stations(self):
        import_polling_station_shapefiles(self)
