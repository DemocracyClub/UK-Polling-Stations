"""
Import Bromsgrove
"""
import sys

from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Bromsgrove
    """
    council_id     = 'E07000234'
    districts_name = 'Electoral Boundaries 2'
    stations_name  = 'Bromsgrove DC and Redditch BC Polling Stations - May 2015 Elections.shp'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'postcode'           : '(postcode not supplied)',
            'address'            : '(address not supplied)'
        }
    
