"""
Import Kensington and Chelsea
"""
from time import sleep

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Kensington and Chelsea Council
    """
    council_id      = 'E09000020'
    addresses_name  = 'referendumstations.csv'
    stations_name   = 'referendumstations.csv'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):
        return "-".join([
            record.districtreference,
            record.bs7666paonstartsuffix,
            record.bs7666paonstartnumber,
        ])

    def station_record_to_dict(self, record):
        # format address
        address = "\n".join([f.strip() for f in [
            record.name,
            record.address1,
            record.address2,
            record.address3,
            record.address4,
            record.address5,
        ] if f != "NULL"])

        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = record.postcode

        location = None
        if int(record.easting) and int(record.northing):
            location = Point(
                int(record.easting),
                int(record.northing),
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
            'internal_council_id': record.districtreference,
            'polling_district_id': record.districtreference,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        address = "\n".join([f.strip() for f in
            [record.addressline1,
            record.addressline2,
            record.addressline3,
            record.addressline4,
            record.addresspostcode,
        ] if f])


        return {
            'address' : address,
            'postcode' : record.addresspostcode.strip(),
            'polling_station_id': record.districtreference,
        }
