from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHO"
    addresses_name = "2025-05-01/2025-02-28T08:34:33.193115/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-02-28T08:34:33.193115/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]
