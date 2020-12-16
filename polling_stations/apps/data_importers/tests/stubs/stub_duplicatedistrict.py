import os
from data_importers.tests.stubs import BaseStubCsvStationsJsonDistrictsImporter


"""
Define a stub implementation of json importer we can run tests against
uses data that will return a duplicate district on
(council_id, internal_council_id) by design
"""


class Command(BaseStubCsvStationsJsonDistrictsImporter):

    srid = 4326
    districts_name = "test.geojson"
    stations_name = "test.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/duplicate_district"
    )
