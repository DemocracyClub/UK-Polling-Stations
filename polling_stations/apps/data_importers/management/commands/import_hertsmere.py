from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HER"
    addresses_name = "2025-05-01/2025-03-12T17:07:55.818621/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-12T17:07:55.818621/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]
