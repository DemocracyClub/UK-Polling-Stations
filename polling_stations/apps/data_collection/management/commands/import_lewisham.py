"""
Import Lewisham
"""

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Lewisham Council
    """
    council_id      = 'E09000023'
    addresses_name  = 'PropertyPostCodePollingStation-Lewisham.csv'
    stations_name   = 'PropertyPostCodePollingStation-Lewisham.csv'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):
        return "-".join([
            record.poll_ref,
            record.polling_pl,
        ])

    def station_record_to_dict(self, record):
        # format address
        address = "\n".join([
            record.polling_pl,
            record.pol_addre,
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = " ".join(address.split(' ')[-2:]).strip().split('\n')[-1]

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
            'internal_council_id': record.poll_ref,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.paon.strip() == '0':
            address = record.streetname.strip()
        else:
            address = " ".join([
                record.paon.strip(),
                record.street_des.strip(),
            ])

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.poll_ref
        }
