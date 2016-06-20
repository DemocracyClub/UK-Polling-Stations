"""
Import Barnet

note: this script takes quite a long time to run
"""

from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Barnet Council
    """
    council_id      = 'E09000003'
    addresses_name  = 'Polling_Place_Postcode_Lookup__23June2016_LBBarnet.CSV'
    stations_name   = 'Polling_Place_Postcode_Lookup__23June2016_LBBarnet.CSV'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):
        return "-".join([
            record.polling_place_name,
            record.polling_place_address_1,
        ])

    def station_record_to_dict(self, record):
        # format address
        address = "\n".join([
            record.polling_place_address_1,
            record.polling_place_address_2,
            record.polling_place_address_3,
            record.polling_place_address_4,
            record.polling_place_postcode,
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = record.polling_place_postcode.strip()

        location = None
        location_data = None
        # no points supplied, so attempt to attach them by geocoding
        try:
            location_data = geocode_point_only(postcode)
        except PostcodeError:
            pass

        if location_data:
            location = Point(
                location_data['wgs84_lon'],
                location_data['wgs84_lat'],
                srid=4326)

        return {
            'internal_council_id': self.get_station_hash(record),
            'postcode' : postcode,
            'address' : address,
            'location' : location,
        }

    def address_record_to_dict(self, record):
        return
        if record.propertynumber.strip() == '0':
            address = record.streetname.strip()
        else:
            address = '%s %s' % (
                record.propertynumber.strip(), record.streetname.strip())

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.pollingplaceid
        }
