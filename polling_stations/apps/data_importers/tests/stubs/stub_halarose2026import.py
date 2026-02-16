import os

from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "AAA"
    addresses_name = "test.csv"
    stations_name = "test.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/halarose_2026_importer"
    )
