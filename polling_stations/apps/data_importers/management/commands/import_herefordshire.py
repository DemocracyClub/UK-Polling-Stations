from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HEF"
    addresses_name = "2023-05-04/2023-04-13T19:43:00.615745/Eros_SQL_Output002.csv"
    stations_name = "2023-05-04/2023-04-13T19:43:00.615745/Eros_SQL_Output002.csv"
    elections = ["2023-05-04"]
