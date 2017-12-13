"""
Import Vale of Glamorgan
"""
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Vale of Glamorgan
    """
    council_id     = 'W06000014'
    districts_name = 'parl.2017-06-08/Version 1/Polling Districts.shp'
    stations_name  = 'parl.2017-06-08/Version 1/Polling Stations.shp'
    elections = ['parl.2017-06-08']

    def district_record_to_dict(self, record):

        # this address is missing from the stations file
        # so put it in an object property where we can
        # pick it up in station_record_to_dict()
        if record[1] == 'FD1':
            self.fd1_address = record[5]

        return {
            'internal_council_id': record[1],
            'name'               : record[2],
            'polling_station_id' : record[1]
        }

    def station_record_to_dict(self, record):

        if record[0] == 'FD1':
            address = self.fd1_address
        else:
            address = record[2]

        return {
            'internal_council_id': record[0],
            'postcode'           : '',
            'address'            : address,
            'polling_district_id': record[0]
        }
