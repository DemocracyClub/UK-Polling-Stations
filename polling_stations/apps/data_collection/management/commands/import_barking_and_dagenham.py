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
    stations_name = 'parl.2017-06-08/Version 1/Polling_Stations2017DemocracyClub'
    elections = ['parl.2017-06-08']
    seen_stations = set()

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):

        address = record[3].strip()
        postcode = " ".join(address.split(' ')[-2:])
        code = record[4].strip()

        if code in self.seen_stations:
            return None

        self.seen_stations.add(code)
        return {
            'internal_council_id': code,
            'polling_district_id': code,
            'postcode' : postcode,
            'address' : address,
        }
