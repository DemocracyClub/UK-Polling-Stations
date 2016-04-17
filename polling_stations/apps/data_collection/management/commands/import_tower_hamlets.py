"""
Import Tower Hamlets
"""
import sys

from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Tower Hamlets
    """
    council_id     = 'E09000030'
    districts_name = 'Polling_Districts_2015'
    stations_name  = 'Polling_Stations_2015.shp'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[3],
            'name': record[4],
            'extra_id': record[0],
            'polling_station_id': record[3]
        }

    def station_record_to_dict(self, record):

        address_parts = [x.strip() for x in record[5].split(',')]
        address = "\n".join(address_parts[:-1])
        postcode = address_parts[-1]
        if postcode == 'Blackwall Way':
            address = "%s\n%s" % (address, postcode)
            postcode = ''
        if postcode[:6] == 'London':
            address = "%s\n%s" % (address, 'London')
            postcode = "%s %s" % (postcode.split(' ')[-2], postcode.split(' ')[-1])

        return {
            'internal_council_id': record[3],
            'postcode'           : postcode,
            'address'            : address,
            'polling_district_id': record[3]
        }
