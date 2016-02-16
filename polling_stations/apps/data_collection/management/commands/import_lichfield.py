"""
Import Lichfield
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter, import_polling_station_shapefiles

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Lichfield Council
    """
    council_id     = 'E07000194'
    districts_name = 'Lichfield_District_Council_Polling_Districts'
    stations_name  = 'Lichfield_District_Council_Polling_Station_Locations.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[2],
        }

    def station_record_to_dict(self, record):
        print(record)
        print(record[1])
        print(record[4])
        print(record[5])

        return {
            'internal_council_id': record[0],
            'postcode'           : record[5],
            'address'            : "\n".join([record[1], record[4]]),
        }
    
    def import_polling_stations(self):
        import_polling_station_shapefiles(self)
