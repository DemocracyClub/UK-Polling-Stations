from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2023-11-23/2023-10-25T13:50:03.120466/Eros_SQL_Output003.csv"
    stations_name = "2023-11-23/2023-10-25T13:50:03.120466/Eros_SQL_Output003.csv"
    elections = ["2023-11-23"]
