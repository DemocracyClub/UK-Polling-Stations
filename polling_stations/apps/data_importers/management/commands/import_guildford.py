from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRT"
    addresses_name = "2023-05-04/2023-03-14T12:03:03.221735/Eros_SQL_Output014.csv"
    stations_name = "2023-05-04/2023-03-14T12:03:03.221735/Eros_SQL_Output014.csv"
    elections = ["2023-05-04"]
