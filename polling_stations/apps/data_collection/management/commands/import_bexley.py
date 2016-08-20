"""
Import Bexley
"""
from time import sleep

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Bexley Council
    """
    council_id      = 'E09000004'
    addresses_name  = 'Copy of GLA POLLING STATION FINDER.csv'
    stations_name   = 'Copy of GLA POLLING STATION FINDER.csv'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):
        return "-".join([
            record.poll_stn_number,
            record.polling_station_name.strip(),
            record.ps_postcode,
        ])

    def station_record_to_dict(self, record):
        # format address
        address = "\n".join([
            record.ps_address_1,
            record.ps_address_2,
            record.ps_address_3,
            record.ps_address_4,
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = record.post_code

        location = None
        if record.northings and record.eastings:
            location = Point(
                float(record.eastings),
                float(record.northings),
                srid=27700)
        else:
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
            'internal_council_id': record.poll_stn_number,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        address = ", ".join([ r.strip() for r in [
            record.address_1,
            record.address_2,
            record.address_3,
            record.address_4,
            record.address_5,
            record.address_6,

        ] if r])

        return {
            'address'           : address,
            'postcode'          : record.post_code.strip(),
            'polling_station_id': record.poll_stn_number
        }
