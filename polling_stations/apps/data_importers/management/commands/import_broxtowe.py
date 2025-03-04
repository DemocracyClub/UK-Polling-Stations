from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRT"
    addresses_name = "2025-05-01/2025-03-04T15:02:27.653222/Eros_SQL_Output003.csv"
    stations_name = "2025-05-01/2025-03-04T15:02:27.653222/Eros_SQL_Output003.csv"
    elections = ["2025-05-01"]
