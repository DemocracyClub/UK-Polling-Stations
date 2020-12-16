import os
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "X01000000"
    addresses_name = "test.csv"
    stations_name = "test.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/halarose_importer"
    )
