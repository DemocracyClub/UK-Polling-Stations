import os
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "X01000000"
    addresses_name = "districts.csv"
    stations_name = "stations.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/dcounts_importer"
    )
