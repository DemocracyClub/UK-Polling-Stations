import os
from data_importers.tests.stubs import BaseStubCsvStationsJsonDistrictsImporter


"""
Define a stub implementation of json importer we can run tests against
csv and geojson both use srid 4326
"""


class Command(BaseStubCsvStationsJsonDistrictsImporter):

    srid = 4326
    districts_name = "test.geojson"
    stations_name = "test_4326.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/json_importer"
    )
