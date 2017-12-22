import os
from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id       = 'X01000000'
    addresses_name   = 'test_weblookup.csv'
    stations_name    = 'test_weblookup.csv'
    base_folder_path = os.path.join(os.path.dirname(__file__), '../fixtures/xpress_importer')
