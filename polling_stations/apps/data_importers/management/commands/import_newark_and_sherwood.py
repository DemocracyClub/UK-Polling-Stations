from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEA"
    addresses_name = "2025-05-01/2025-03-17T15:39:24.857102/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-17T15:39:24.857102/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]
