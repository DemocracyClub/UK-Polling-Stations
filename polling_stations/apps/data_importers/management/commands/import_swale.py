from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWL"
    addresses_name = "2025-05-01/2025-03-11T12:31:18.335513/Eros_SQL_Output002.csv"
    stations_name = "2025-05-01/2025-03-11T12:31:18.335513/Eros_SQL_Output002.csv"
    elections = ["2025-05-01"]
