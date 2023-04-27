from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEA"
    addresses_name = "2023-05-04/2023-04-26T16:10:23.079677/Eros_SQL_Output003.csv"
    stations_name = "2023-05-04/2023-04-26T16:10:23.079677/Eros_SQL_Output003.csv"
    elections = ["2023-05-04"]
