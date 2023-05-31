from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2023-07-04/2023-05-31T14:59:32.696409/Eros_SQL_Output013.csv"
    stations_name = "2023-07-04/2023-05-31T14:59:32.696409/Eros_SQL_Output013.csv"
    elections = ["2023-07-04"]
