from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LEE"
    addresses_name = "2025-05-29/2025-05-19T11:04:34.585409/Eros_SQL_Output001.csv"
    stations_name = "2025-05-29/2025-05-19T11:04:34.585409/Eros_SQL_Output001.csv"
    elections = ["2025-05-29"]
