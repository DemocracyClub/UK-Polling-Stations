import json

import shapefile

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseShpImporter
from pollingstations.models import PollingStation, PollingDistrict


class Command(BaseShpImporter):
    srid = 27700


    def district_record_to_dict(self, record):
        return {
            'council': self.council,
            'name': record[1],
            'internal_council_id': record[2],
        }


    def station_record_to_dict(self, record):
        return {
            'council': self.council,
            'internal_council_id': record[2],
            'address': record[3].decode('cp1252'),
        }


