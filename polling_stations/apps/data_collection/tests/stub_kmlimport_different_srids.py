import os
from django.contrib.gis.geos import Point, GEOSGeometry
from data_collection.management.commands import BaseKamlImporter


"""
Define a stub implementation of kml importer we can run tests against
kml uses srid 4326, csv uses srid 27700
"""
class Command(BaseKamlImporter):

    srid             = 27700
    districts_srid   = 4326
    council_id       = 'X01000000'
    districts_name   = 'test.kml'
    stations_name    = 'test_27700.csv'
    base_folder_path = os.path.join(os.path.dirname(__file__), 'fixtures/kml_importer')

    def district_record_to_dict(self, record):
        geojson = record.geom.geojson
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))
        return {
            'internal_council_id': record['Name'].value,
            'name'               : record['Name'].value,
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.east), float(record.north), srid=self.get_srid())
        return {
            'council':             self.council,
            'internal_council_id': record.internal_council_id,
            'postcode':            record.postcode,
            'address':             record.address,
            'location':            location
        }
