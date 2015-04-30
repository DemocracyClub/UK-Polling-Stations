"""
Import Edinburgh
"""
import sys

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Edinburgh
    """
    council_id     = 'S12000036'
    districts_name = 'Polling district boundaries 2014'
    stations_name  = 'Polling places 2014.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'postcode'           : record[1],
            'address'            : "\n".join([record[0], record[2], record[3]])
        }
    
