"""
Import Runnymede
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import (
    BaseCsvStationsShpDistrictsImporter,
    import_polling_station_shapefiles
)

class Command(BaseCsvStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Runnymede Council
    """
    council_id     = 'E07000212'
    districts_name = 'RBC_Polling_Districts'
    stations_name  = 'RBC_Polling_Stations.shp'
    elections      = ['parl.2015-05-07']

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
