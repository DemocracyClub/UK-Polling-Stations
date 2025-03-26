from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "DAR"
    addresses_name = "2025-05-01/2025-03-26T12:58:37.459986/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-26T12:58:37.459986/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]
