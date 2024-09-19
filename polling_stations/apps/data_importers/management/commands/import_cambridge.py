from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2024-09-12/2024-08-19T14:53:32.358059/Eros_SQL_Output018.csv"
    stations_name = "2024-09-12/2024-08-19T14:53:32.358059/Eros_SQL_Output018.csv"
    elections = ["2024-09-12"]
