from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from data_finder.helpers import geocode_point_only, PostcodeError

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000171'
    addresses_name = 'Democracy_Club__04May2017 (7).tsv'
    stations_name = 'Democracy_Club__04May2017 (7).tsv'
    elections = [
        'local.nottinghamshire.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):
        address = self.get_station_address(record)
        location = self.get_station_point(record)
        return {
            'internal_council_id': getattr(record, self.station_id_field).strip(),
            'postcode'           : '',
            'address'            : address.strip(),
            'location'           : location
        }

    def get_postcode(self, record):
        fields = [
            'polling_place_postcode',
            'polling_place_address_4',
        ]
        for field in fields:
            if getattr(record, field):
                return getattr(record, field).strip()
        return None

    def get_station_point(self, record):
        location = None
        postcode = self.get_postcode(record)
        if not postcode:
            return None

        try:
            location_data = geocode_point_only(postcode)
            location = Point(
                location_data['wgs84_lon'],
                location_data['wgs84_lat'],
                srid=4326)
        except PostcodeError:
            location = None

        return location

    station_address_fields = [
        'polling_place_name',
        'polling_place_address_1',
        'polling_place_address_2',
        'polling_place_address_3',
        'polling_place_address_4',
        'polling_place_postcode',
    ]