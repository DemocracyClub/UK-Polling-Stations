"""
Import Bromley
"""
from time import sleep

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Bromley Council
    """
    private = True
    council_id      = 'E09000006'
    addresses_name  = 'addresses.csv'
    stations_name   = 'stations.csv'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):
        address = record.situation_of_polling_station
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        location = None
        location_data = None
        if record.postcode_if_available:
            try:
                location_data = geocode_point_only(postcode_if_available)
            except PostcodeError:
                pass

            if location_data:
                location = Point(
                    location_data['wgs84_lon'],
                    location_data['wgs84_lat'],
                    srid=4326)

        desc = record.description_of_persons_entitled_to_vote
        district = desc.split('-')[0].strip()

        return {
            'internal_council_id': district,
            'polling_district_id': district,
            'postcode'           : None,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        address = record.address

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.district
        }
