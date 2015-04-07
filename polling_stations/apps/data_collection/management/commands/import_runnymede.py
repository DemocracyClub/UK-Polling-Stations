"""
Import Runnymede
"""
from django.contrib.gis.geos import Point
import ffs

from data_collection.management.commands import BaseShpImporter, import_polling_station_shapefiles

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Runnymede Council
    """
    council_id     = 'E07000212'
    districts_name = 'RBC_Polling_Districts'
    stations_name  = 'RBC_Polling_Stations.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[-1],
            'name': record[0],
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[-1],
            'postcode'           : '(No postcode supplied)',
            'address'            : record[1],
        }
    
    def import_polling_stations(self):
        import_polling_station_shapefiles(self)
