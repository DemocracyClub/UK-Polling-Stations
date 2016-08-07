"""
Import Greenwich
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode, geocode_point_only, PostcodeError
from addressbase.models import Address


class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Greenwich Council
    """
    council_id = 'E09000011'
    addresses_name = 'Addresses.csv'
    stations_name = 'PollingStations.csv'
    csv_delimiter = ','
    elections = [
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):
        # format address
        address = record.pollingstation
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()
        postcode = " ".join(address.split(' ')[-2:])

        location = None
        if float(record.lat) and float(record.lng):
            location = Point(
                float(record.lng),
                float(record.lat),
                srid=4326)
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
            'internal_council_id': record.stationcode,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):
        if record.pao.strip() == '0':
            address = record.streetname.strip()
        else:
            address = " ".join([
                record.pao.strip(),
                record.streetname.strip(),
                record.locality.strip(),
                record.posttown.strip(),

            ])

        return {
            'address'           : address,
            'postcode'          : record.postcode.strip(),
            'polling_station_id': record.stationcode
        }
