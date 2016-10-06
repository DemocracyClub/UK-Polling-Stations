"""
Import Sheffield
"""
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Sheffield
    """
    council_id     = 'E08000019'
    districts_name = 'SCCPollingDistricts2015'
    stations_name  = 'SCCPollingStations2015.shp'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'extra_id':            record[0],
            'name':                record[1],
        }

    def station_record_to_dict(self, record):

        address = record[1]

        # remove postcode from end of address if present
        postcode_offset = -len(record[2])
        if address[postcode_offset:] == record[2]:
            address = address[:postcode_offset].strip()

        # remove trailing comma if present
        if address[-1:] == ',':
            address = address[:-1]

        # replace commas with \n
        address = "\n".join(map(lambda x: x.strip(), address.split(',')))

        return {
            'internal_council_id': record[0],
            'postcode'           : record[2],
            'address'            : address,
            'polling_district_id': record[-1]
        }
