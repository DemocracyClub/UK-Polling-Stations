from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MAS"
    addresses_name = "2023-05-04/2023-03-23T16:11:56.327479/Eros_SQL_Output005.csv"
    stations_name = "2023-05-04/2023-03-23T16:11:56.327479/Eros_SQL_Output005.csv"
    elections = ["2023-05-04"]
