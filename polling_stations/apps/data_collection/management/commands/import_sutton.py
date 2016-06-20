"""
Import Sutton
"""
from time import sleep

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Sutton Council
    """
    council_id      = 'E09000029'
    addresses_name  = 'Sutton Polling District Addresses.csv'
    stations_name   = 'Sutton Polling District Addresses.csv'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):

        return "-".join([
            record.pollingstationid,
        ])

    def station_record_to_dict(self, record):
        address = record.pollingstationdetails

        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = " ".join(address.split(' ')[:2])

        location = None
        location_data = None
        if float(record.pollingstationxref) and float(record.pollingstationyref):
            location = Point(
                float(record.pollingstationxref),
                float(record.pollingstationyref),
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
            'internal_council_id': record.pollingstationid,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        address = ", ".join([f.strip() for f in [
            record.paonumber,
            record.paoname,
            record.streetname,
            record.locality,
            record.posttown,
            record.county,
        ] if f])

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.pollingstationid
        }
