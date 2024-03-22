from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ALL"
    addresses_name = "2024-05-02/2024-03-22T16:12:07.250021/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-22T16:12:07.250021/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
