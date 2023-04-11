from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TAN"
    addresses_name = "2023-05-04/2023-04-11T12:32:00.173227/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-04-11T12:32:00.173227/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]
