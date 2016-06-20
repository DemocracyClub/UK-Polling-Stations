"""
Import Brent
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Brent Council
    """
    council_id = 'E09000005'
    addresses_name = '2016/Brent polling station GIS data.csv'
    stations_name = '2016/Brent polling station GIS data.csv'
    csv_delimiter = ','
    elections = ['ref.2016-06-23']

    def get_station_hash(self, record):
        return "-".join([
            record.stationuprn,
            record.premise_p_code,
            record.premise_name,
        ])

    def station_record_to_dict(self, record):
        # format address
        address = "\n".join([
            record.premise_name,
            record.premise_add1,
            record.premise_add2,
            record.premise_add3,
            record.premise_add4,
            record.premise_add5,
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = record.premise_p_code
        location = None
        location_data = None
        # no points supplied, so attempt to attach them by geocoding
        if len(postcode) > 5:
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
            'internal_council_id': record.stationuprn,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):

        address = ", ".join([f.strip() for f in [
            record.house_name,
            record.house_no,
            record.street_name,
            record.address_line_1,
            record.address_line_2,
            record.address_line_3,
            record.address_line_4,
            record.address_line_5,
        ] if f])

        return {
            'address'           : address,
            'postcode'          : record.post_code.strip(),
            'polling_station_id': record.stationuprn
        }
