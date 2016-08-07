"""
Import Barking-and-Dagenham
"""
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Barking-and-Dagenham
    """
    council_id = 'E09000002'
    districts_name = 'Barking_n_Dag_completed_PDs_region_updated/Barking_n_Dag_completed_PDs_region_updated'
    stations_name = 'Polling_Stations2016/Polling_Stations2016'
    elections = ['ref.2016-06-23']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        postcode = " ".join(record[3].split(' ')[-2:])
        return {
            'internal_council_id': record[1],
            'polling_district_id': record[4],
            'postcode' : postcode,
            'address' : record[3]
        }
