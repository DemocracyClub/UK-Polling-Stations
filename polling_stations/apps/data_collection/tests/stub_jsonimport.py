import os
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsJsonDistrictsImporter


"""
Define a stub implementation of json importer we can run tests against
csv and geojson both use srid 4326
"""
class Command(BaseCsvStationsJsonDistrictsImporter):

    srid             = 4326
    council_id       = 'X01000000'
    districts_name   = 'test.geojson'
    stations_name    = 'test_4326.csv'
    base_folder_path = os.path.join(os.path.dirname(__file__), 'fixtures/json_importer')

    def district_record_to_dict(self, record):
        properties = record['properties']
        return {
            'council':             self.council,
            'internal_council_id': properties['id'],
            'name':                properties['name']
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.lng), float(record.lat), srid=self.get_srid())
        return {
            'council':             self.council,
            'internal_council_id': record.internal_council_id,
            'postcode':            record.postcode,
            'address':             record.address,
            'location':            location
        }
