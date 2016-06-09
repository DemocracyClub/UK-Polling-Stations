"""
Import Hounslow

note: this script takes quite a long time to run
"""
from time import sleep
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, PostcodeError

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Hounslow Council
    """
    council_id      = 'E09000018'
    addresses_name  = 'Hounslow_polling_station_export-2016-06-06.csv'
    stations_name   = 'polling_stations.csv'
    elections       = [
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):
        location = Point(float(record.cntr_x), float(record.cntr_y), srid=27700)

        # format address and postcode
        address = record.polling_station_address
        address_parts = address.split(', ')
        address_parts = [x.strip(' ') for x in address_parts]
        if address_parts[-1][:2] == 'TW' or\
           address_parts[-1][:2] == 'UB' or\
           address_parts[-1][:2] == 'W3' or\
           address_parts[-1][:2] == 'W4' or\
           address_parts[-1][:2] == 'W5':
            postcode = address_parts[-1]
            del(address_parts[-1])
        else:
            postcode = ''
        address = "\n".join(address_parts)

        return {
            'internal_council_id': record.polling_station_number.strip(),
            'postcode'           : postcode,
            'address'            : "%s\n%s" % (record.polling_station_name, address),
            'location'           : location
        }

    def address_record_to_dict(self, record):

        # discard and records without a postcode
        # the user won't be able to search for them anyway
        if not record.housepostcode:
            return None

        # format address
        address1 = "%s %s %s %s %s" % (record.housename, record.housenumber, record.substreetname, record.streetnumber, record.streetname)
        address1 = ' '.join(address1.strip().split())

        address = "\n".join([
            address1,
            record.locality,
            record.town,
            record.adminarea,
        ]).strip()
        address = ", ".join(address.split("\n"))

        return {
            'address'           : address,
            'postcode'          : record.housepostcode,
            'polling_station_id': record.pollingstationnumber
        }
