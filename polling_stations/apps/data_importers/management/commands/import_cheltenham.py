from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHT"
    addresses_name = "2024-07-04/2024-06-22T17:50:28.833358/Eros_SQL_Output009.csv"
    stations_name = "2024-07-04/2024-06-22T17:50:28.833358/Eros_SQL_Output009.csv"
    elections = ["2024-07-04"]
