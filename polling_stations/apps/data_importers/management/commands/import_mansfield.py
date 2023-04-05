from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MAS"
    addresses_name = "2023-05-04/2023-04-05T14:34:48.372992/Eros_SQL_Output006.csv"
    stations_name = "2023-05-04/2023-04-05T14:34:48.372992/Eros_SQL_Output006.csv"
    elections = ["2023-05-04"]
