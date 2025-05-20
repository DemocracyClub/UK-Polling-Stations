from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SLK"
    addresses_name = "2025-06-05/2025-05-20T09:21:33.949450/Eros_SQL_Output004.csv"
    stations_name = "2025-06-05/2025-05-20T09:21:33.949450/Eros_SQL_Output004.csv"
    elections = ["2025-06-05"]
