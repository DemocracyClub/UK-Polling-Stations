from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WEW"
    addresses_name = "2025-05-01/2025-03-24T11:28:50.310602/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-24T11:28:50.310602/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]
