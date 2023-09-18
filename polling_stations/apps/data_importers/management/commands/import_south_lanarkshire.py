from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SLK"
    addresses_name = "2023-10-05/2023-09-14T15:44:11.058187/Eros_SQL_Output003.csv"
    stations_name = "2023-10-05/2023-09-14T15:44:11.058187/Eros_SQL_Output003.csv"
    elections = ["2023-10-05"]
