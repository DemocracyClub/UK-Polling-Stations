from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError
from data_collection.addresshelpers import (
    format_residential_address,
    format_polling_station_address
)


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id      = 'E08000022'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy Club.csv'
    stations_name   = 'local.2018-05-03/Version 1/Democracy Club.csv'
    elections       = ['local.2018-05-03']

    def get_station_hash(self, record):
        return "-".join([
            record.col12.strip(),
        ])

    def get_station_address(self, record):
        return format_polling_station_address([
            record.col23.strip(),
            record.col24.strip(),
            record.col25.strip(),
            record.col26.strip(),
            record.col27.strip(),
        ])

    def get_station_point(self, record):
        postcode = record.col32.strip()
        if postcode == '':
            return None

        try:
            location_data = geocode_point_only(postcode)
            location = location_data.centroid
        except PostcodeError:
            location = None
        return location

    def station_record_to_dict(self, record):
        location = self.get_station_point(record)
        return {
            'internal_council_id': record.col12.strip(),
            'postcode'           : record.col32.strip(),
            'address'            : self.get_station_address(record),
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.col22.strip() == '47237285':
            return None

        address = format_residential_address([
            record.col13.strip(),
            record.col14.strip(),
            record.col15.strip(),
            record.col16.strip(),
            record.col17.strip()
        ])
        return {
            'address'           : address.strip(),
            'postcode'          : record.col21.strip(),
            'polling_station_id': record.col12.strip(),
            'uprn'              : record.col22.strip(),
        }
