"""
Import Merthyr Tydfil

note: this script takes quite a long time to run
"""
from time import sleep
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, PostcodeError
from data_collection.google_geocoding_api_wrapper import (
    GoogleGeocodingApiWrapper,
    PostcodeNotFoundException
)

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Merthyr Tydfil
    """
    council_id      = 'W06000024'
    addresses_name  = 'Merthyr Tydfil UPRN Numbers.csv'
    stations_name   = 'Merthyr Tydfil UPRN Numbers.csv'

    known_stations = set()

    def station_record_to_dict(self, record):
        unique_station_id = "-".join((
            record.polling_district,
            record.polling_station,
            record.polling_station_postcode,
        ))

        if unique_station_id in self.known_stations:
            return None

        address = record.polling_station
        postcode = record.polling_station_postcode

        if not postcode:
            gwrapper = GoogleGeocodingApiWrapper(address, self.council_id, 'UTA')
            try:
                postcode = gwrapper.address_to_postcode()
            except PostcodeNotFoundException:
                postcode = ''


        """
        No grid references were supplied, so attempt to
        derive a grid ref from postcode if we have that
        """
        if postcode:
            try:
                sleep(1.3) # ensure we don't hit mapit's usage limit
                gridref = geocode(postcode)
                location = Point(
                    gridref['wgs84_lon'],
                    gridref['wgs84_lat'],
                    srid=4326
                )
            except PostcodeError:
                location = None
        else:
            location = None

        self.known_stations.add(unique_station_id)

        return {
            'internal_council_id': record.polling_district,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        address = record.property
        postcode = address.split(',')[-1].strip()
        address = address.replace(postcode, '').strip(', ')

        return {
            'address'           : address,
            'postcode'          : postcode,
            'polling_station_id': record.polling_district
        }
