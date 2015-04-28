"""
Import Wokingham Polling stations
"""

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Wokingham Council
    """
    council_id     = 'E06000020'
    districts_name = 'Polling_Districts'
    stations_name  = 'Polling_Stations.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[2],
            'name': record[1],
            'polling_station_id': record[2]
        }

    def station_record_to_dict(self, record):
        print record
        return {
            'internal_council_id': record[1],
            'postcode'           : record[3].split(',')[-1],
            'address'            : "\n".join(record[3].split(',')[:-1]),
        }
