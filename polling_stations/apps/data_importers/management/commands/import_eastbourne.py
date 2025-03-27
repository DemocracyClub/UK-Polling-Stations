from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EAS"
    addresses_name = "2025-05-01/2025-03-27T11:08:14.165552/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-27T11:08:14.165552/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]
