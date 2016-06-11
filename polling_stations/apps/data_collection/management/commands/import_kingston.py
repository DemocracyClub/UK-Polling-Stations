"""
Import Kingston

note: this script takes quite a long time to run
"""
from time import sleep
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, PostcodeError

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Kingston Council
    """
    council_id      = 'E09000021'
    addresses_name  = 'rev02-2016/PropertyPostCodePollingStationWebLookup-2016-06-23 (1).csv'
    stations_name   = 'rev02-2016/Polling_station_addresses_coordinates_and_UPRN (2).csv'
    csv_encoding    = 'latin-1'
    elections       = [
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):
        location = Point(int(record.eastings), int(record.northings), srid=27700)

        # format address and postcode
        address = record.location
        address_parts = address.split(', ')
        address_parts = [x.strip(' ') for x in address_parts]
        postcode = address_parts[-1]
        del(address_parts[-1])
        address = "\n".join(address_parts)

        return {
            'internal_council_id': record.other_info.strip(),
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        postcode = record.postcode.strip()
        if record.propertynumber.strip() == '0':
            address = record.streetname.strip()
        else:
            address = '%s %s' % (record.propertynumber.strip(), record.streetname.strip())

        return {
            'address'           : address,
            'postcode'          : postcode,
            'polling_station_id': record.pollingdistrictreference
        }
