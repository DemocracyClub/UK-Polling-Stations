import os
from django.contrib.gis.geos import Point
from data_importers.tests.stubs import BaseStubCsvStationsKmlDistrictsImporter


"""
Define a stub implementation of kml importer we can run tests against
csv and kml both use srid 4326
"""


class Command(BaseStubCsvStationsKmlDistrictsImporter):

    srid = 4326
    districts_name = "test.kml"
    stations_name = "test_4326.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/kml_importer"
    )

    def station_record_to_dict(self, record):
        location = Point(float(record.lng), float(record.lat), srid=self.get_srid())
        return {
            "council": self.council,
            "internal_council_id": record.internal_council_id,
            "postcode": record.postcode,
            "address": record.address,
            "location": location,
        }
