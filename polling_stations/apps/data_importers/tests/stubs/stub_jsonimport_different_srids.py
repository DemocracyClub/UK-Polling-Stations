import os
from django.contrib.gis.geos import Point
from data_importers.tests.stubs import BaseStubCsvStationsJsonDistrictsImporter


"""
Define a stub implementation of json importer we can run tests against
goejosn uses srid 4326, csv uses srid 27700
"""


class Command(BaseStubCsvStationsJsonDistrictsImporter):

    srid = 27700
    districts_srid = 4326
    districts_name = "test.geojson"
    stations_name = "test_27700.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/json_importer"
    )

    def station_record_to_dict(self, record):
        location = Point(float(record.east), float(record.north), srid=self.get_srid())
        return {
            "council": self.council,
            "internal_council_id": record.internal_council_id,
            "postcode": record.postcode,
            "address": record.address,
            "location": location,
        }
