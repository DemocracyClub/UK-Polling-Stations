from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAY"
    addresses_name = "2024-05-02/2024-03-22T14:36:48.765501/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-22T14:36:48.765501/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
