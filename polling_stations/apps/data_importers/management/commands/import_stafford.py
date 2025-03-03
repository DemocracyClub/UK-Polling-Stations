from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "STA"
    addresses_name = "2025-05-01/2025-03-03T11:42:30.038880/Eros_SQL_Output028.csv"
    stations_name = "2025-05-01/2025-03-03T11:42:30.038880/Eros_SQL_Output028.csv"
    elections = ["2025-05-01"]
