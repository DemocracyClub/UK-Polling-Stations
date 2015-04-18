"""
Import COUNCIL
"""
import sys

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from COUNCIL
    """
    council_id     = 'your_councilid'
    districts_name = 'name_without_.shp'
    stations_name  = 'your.shp'

    def district_record_to_dict(self, record):
        print 'District:', record
        sys.exit(1)
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        print 'Station', record
        sys.exit(1)
        return {
            'internal_council_id': record[0],
            'postcode'           : record[1],
            'address'            : record[2]
        }
    
