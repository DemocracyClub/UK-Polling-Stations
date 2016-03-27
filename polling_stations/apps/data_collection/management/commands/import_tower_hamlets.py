"""
Import Tower Hamlets
"""
import sys

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Tower Hamlets
    """
    council_id     = 'E09000030'
    districts_name = 'Polling_Districts_2015'
    stations_name  = 'Polling_Stations_2015.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[3],
            'name': record[4],
            'extra_id': record[0],
            'polling_station_id': record[3]
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[3],
            'postcode'           : self.postcode_from_address(record[-1]),
            'address'            : "\n".join(record[-1].split(',')[:-1]),
            'polling_district_id': record[3]
        }
    
