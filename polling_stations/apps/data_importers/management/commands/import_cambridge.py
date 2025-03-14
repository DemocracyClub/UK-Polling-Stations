from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2025-05-01/2025-03-14T17:10:10.195808/Eros_SQL_Output002.csv"
    stations_name = "2025-05-01/2025-03-14T17:10:10.195808/Eros_SQL_Output002.csv"
    elections = ["2025-05-01"]
