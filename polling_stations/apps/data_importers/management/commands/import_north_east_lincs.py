from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = "2025-05-01/2025-03-03T14:56:37.387375/Eros_SQL_Output004.csv"
    stations_name = "2025-05-01/2025-03-03T14:56:37.387375/Eros_SQL_Output004.csv"
    elections = ["2025-05-01"]
