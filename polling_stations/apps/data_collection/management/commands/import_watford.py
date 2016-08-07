"""
Import Watford
"""
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Watford
    """
    council_id     = 'E07000103'
    districts_name = 'Watford_Polling_Districts'
    stations_name  = 'Watford_Polling_Stations.shp'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[2],
            'name': record[2],
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'postcode'           : record[5],
            'address'            : "\n".join([record[3], record[4]]),
            'polling_district_id': record[2]
        }
