"""
Import Wokingham Polling stations
"""

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Wokingham Council
    """
    council_id     = 'E06000037'
    districts_name = 'polling_districts'
    stations_name  = 'polling_places.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[4],
            'name': record[2],
            'polling_station_id': record[6]
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[4],
            'postcode'           : record[5].split(',')[-1],
            'address'            : "\n".join(record[5].split(',')[:-1]),
        }
