from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEA"
    addresses_name = "2024-05-02/2024-03-27T14:37:19.282513/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-27T14:37:19.282513/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]
