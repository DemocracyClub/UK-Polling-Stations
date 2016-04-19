"""
Import South Cambridge
"""
import sys

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from South Cambridge
    """
    srid = 4326
    council_id     = 'E07000012'
    districts_name = 'Polling Districts for Twitter_region'
    stations_name  = 'Polling Stations for Twitter_point.shp'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'name': record[0],
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'postcode'           : self.postcode_from_address(record[0]).strip(),
            'address'            : self.string_to_newline_addr(record[0])
        }
    
