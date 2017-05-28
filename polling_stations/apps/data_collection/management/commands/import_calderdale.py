from django.contrib.gis.geos import Point
from django.db import connection
from pollingstations.models import PollingDistrict
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter
from data_finder.helpers import geocode_point_only, PostcodeError


class Command(BaseShpStationsShpDistrictsImporter):
    council_id       = 'E08000033'
    districts_name   = 'parl.2017-06-08/Version 2/Polling Districts.shp'
    stations_name    = 'parl.2017-06-08/Version 2/polling-stations.shp'
    elections        = ['parl.2017-06-08']

    def parse_string(self, text):
        try:
            return text.strip().decode('utf-8')
        except AttributeError:
            return text.strip()

    def district_record_to_dict(self, record):
        # exclude duplicate/ambiguous code
        if str(record[0]).strip() == 'DC':
            return None

        return {
            'internal_council_id': str(record[0]).strip(),
            'name': str(record[1]).strip(),
            'polling_station_id': str(record[0]).strip(),
        }

    def station_record_to_dict(self, record):
        code = self.parse_string(record[1])
        address = self.parse_string(record[0])

        if code == '' and address == '':
            return None

        return {
            'internal_council_id': code,
            'address': address,
            'postcode': '',
        }
