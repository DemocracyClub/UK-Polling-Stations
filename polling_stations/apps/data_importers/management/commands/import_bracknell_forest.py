from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRC"
    addresses_name = "2024-07-04/2024-05-23T17:44:58.932762/Eros_SQL_Output005.csv"
    stations_name = "2024-07-04/2024-05-23T17:44:58.932762/Eros_SQL_Output005.csv"
    elections = ["2024-07-04"]
