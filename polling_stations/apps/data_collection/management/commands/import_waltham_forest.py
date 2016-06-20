"""
Import Waltham Forest

note: this script takes quite a long time to run
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode_point_only, PostcodeError

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Waltham Forest Council
    """
    council_id      = 'E09000031'
    addresses_name  = 'Waltham Forest PropertyPostCodePollingStationWebLookup-2016-06-06 (1).tsv'
    stations_name   = 'Waltham Forest polling station locations.tsv'
    csv_delimiter   = '\t'
    elections       = [
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):

        # postcode
        if record.postcode == 'rd Lane':
            postcode = ''
        else:
            postcode = record.postcode.strip()

        # point
        if record.easting and record.northing:
            location = Point(float(record.easting), float(record.northing), srid=27700)
        else:
            # no points supplied, so attempt to attach one by geocoding
            try:
                gridref = geocode_point_only(postcode)
                location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None

        # format address
        address = record.address
        address_parts = address.split(', ')
        address_parts = [x.strip(' ') for x in address_parts]
        if address_parts[-1] == postcode:
            del(address_parts[-1])
        address = "%s\n%s" % (record.name, "\n".join(address_parts))

        return {
            'internal_council_id': record.district,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.propertynumber.strip() == '0':
            address = record.streetname.strip()
        else:
            address = '%s %s' % (record.propertynumber.strip(), record.streetname.strip())

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.pollingdistrictreference
        }
