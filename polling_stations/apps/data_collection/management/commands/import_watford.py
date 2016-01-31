"""
Import Watford
"""
from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Watford
    """
    council_id     = 'E07000103'
    districts_name = 'Watford_Polling_Districts'
    stations_name  = 'Watford_Polling_Stations.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[2],
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'postcode'           : record[5],
            'address'            : "\n".join([record[3], record[4]])
        }
