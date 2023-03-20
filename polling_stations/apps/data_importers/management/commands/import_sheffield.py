from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SHF"
    addresses_name = "2023-05-04/2023-03-20T15:52:31.211109/Eros_SQL_Output009.csv"
    stations_name = "2023-05-04/2023-03-20T15:52:31.211109/Eros_SQL_Output009.csv"
    elections = ["2023-05-04"]
