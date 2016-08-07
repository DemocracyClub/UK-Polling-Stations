"""
Import Southwark
"""
from time import sleep

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Southwark Council
    """
    council_id      = 'E09000033'
    addresses_name  = 'Westminster polling_station_export-2016-03-01.csv'
    stations_name   = 'Westminster polling_station_export-2016-03-01.csv'
    csv_delimiter   = ','
    elections       = [
        'ref.2016-06-23'
    ]

    def get_station_hash(self, record):
        return "-".join([
            record.pollingstationaddress_1,
            record.pollingstationnumber,
            record.pollingstationname,
        ])

    def station_record_to_dict(self, record):
        # format address
        address = "\n".join([
            record.pollingstationaddress_1,
            record.pollingstationaddress_2,
            record.pollingstationaddress_3,
            record.pollingstationaddress_4,
            record.pollingstationaddress_5,
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = record.pollingstationpostcode
        if postcode == "n/a":
            return

        location_data = None
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
            'internal_council_id': record.pollingstationnumber,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        address = ", ".join([ r.strip() for r in [
            record.housename,
            record.housenumber,
            record.substreetname,
            record.streetname,
            record.locality,
            record.town,
            record.adminarea,
        ] if r])

        return {
            'address'           : address,
            'postcode'          : record.housepostcode.strip(),
            'polling_station_id': record.pollingstationnumber
        }
