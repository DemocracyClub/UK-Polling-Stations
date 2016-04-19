"""
Import Rhondda Cynon Taf

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
    Imports the Polling Station data from Rhondda Cynon Taf
    """
    council_id      = 'W06000016'
    addresses_name  = 'PROPERTYLISTINGFORDEMOCRACYCLUB.csv'
    stations_name   = 'POLLINGSTATIONS8MARCH2016.csv'
    elections       = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):

        # format address
        address = "\n".join([
            record.address1,
            record.address2,
            record.address3,
            record.address4,
            record.address5
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")
        # remove trailing "\n" if present
        if address[-1:] == '\n':
            address = address[:-1]


        # attempt to attach postcode if missing
        postcode = record.postcode
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
        sleep(1.3) # ensure we don't hit mapit's usage limit
        if postcode:
            try:
                gridref = geocode(postcode)
                location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None
        else:
            location = None


        return {
            'internal_council_id': record.polling_district,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):

        # format address
        address = ", ".join([
            record.address1,
            record.address2,
            record.address3,
            record.address4,
            record.address5,
            record.address6,
        ])
        while ", , " in address:
            address = address.replace(", , ", ", ")
        # remove trailing ", " if present
        if address[-2:] == ', ':
            address = address[:-2]


        return {
            'address'           : address,
            'postcode'          : record.postcode,
            'polling_station_id': record.district
        }
