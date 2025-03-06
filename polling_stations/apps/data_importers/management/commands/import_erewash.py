from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ERE"
    addresses_name = "2025-05-01/2025-03-06T13:02:10.485125/Eros_SQL_Output005.csv"
    stations_name = "2025-05-01/2025-03-06T13:02:10.485125/Eros_SQL_Output005.csv"
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
