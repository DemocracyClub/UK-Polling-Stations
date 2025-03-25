from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "OXO"
    addresses_name = "2025-05-01/2025-03-25T12:23:22.273024/Eros_SQL_Output003.csv"
    stations_name = "2025-05-01/2025-03-25T12:23:22.273024/Eros_SQL_Output003.csv"
    elections = ["2025-05-01"]
