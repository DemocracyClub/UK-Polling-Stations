"""
Import Tower Hamlets
"""
from time import sleep

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Tower Hamlets Council
    """
    council_id      = 'E09000030'
    addresses_name  = '2016/Polling Stations with Addresses.csv'
    stations_name   = '2016/Polling Stations with Addresses.csv'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):
        return "-".join([
            record.station_na,
            record.code,
            record.polling_na,
        ])

    def station_record_to_dict(self, record):
        if not record.polling_na:
            return
        # format address
        address = record.station_na
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()
        postcode = " ".join(address.split(' ')[-2:]).strip().split('\n')[-1]

        location = None
        if float(record.polling_station_x) and float(record.polling_station_y):
            if "Shapla Primary School" in address:
                location = Point(
                    -0.066990,
                    51.510020,
                    srid=4326
                )
            else:
                location = Point(
                    float(record.polling_station_x),
                    float(record.polling_station_y),
                    srid=27700)
        else:
            # no points supplied, so attempt to attach them by geocoding
            try:
                location_data = geocode_point_only(postcode)
                location = location_data.centroid
            except PostcodeError:
                pass

        return {
            'internal_council_id': record.code,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        return {
            'address'           : record.fulladdress.strip(),
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.code
        }
