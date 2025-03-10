from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHT"
    addresses_name = "2025-05-01/2025-02-28T13:01:36.708211/Eros_SQL_Output007.csv"
    stations_name = "2025-05-01/2025-02-28T13:01:36.708211/Eros_SQL_Output007.csv"
    elections = ["2025-05-01"]
