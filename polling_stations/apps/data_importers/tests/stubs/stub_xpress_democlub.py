import os
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "X01000000"
    addresses_name = "test_democlub.csv"
    stations_name = "test_democlub.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/xpress_importer"
    )
