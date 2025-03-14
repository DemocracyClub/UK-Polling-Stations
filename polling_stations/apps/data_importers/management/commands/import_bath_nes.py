from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BAS"
    addresses_name = "2025-05-01/2025-03-06T16:39:35.399261/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-06T16:39:35.399261/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]
