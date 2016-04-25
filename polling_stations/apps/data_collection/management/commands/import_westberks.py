"""
Import West Berkshire Polling stations
"""

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from West Berkshire Council
    """
    council_id     = 'E06000037'
    districts_name = 'rev02-2016/PollingDistricts'
    stations_name  = 'rev02-2016/PollingStations.shp'
    elections      = [
        'pcc.2016-05-05',
        'ref.2016-06-23'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[4],
            'name': "%s - %s" % (record[2], record[4]),
            'polling_station_id': record[4]
        }

    def station_record_to_dict(self, record):

        address_parts = record[5].split(' ')
        if address_parts[-1] != 'Newbury' and address_parts[-1] != 'Reading':
            postcode = "%s %s" % (address_parts[-2], address_parts[-1])
            del(address_parts[-1])
            del(address_parts[-1])
        else:
            postcode = ''

        address = " ".join(address_parts)

        return {
            'internal_council_id': record[4],
            'postcode'           : postcode,
            'address'            : address
        }
