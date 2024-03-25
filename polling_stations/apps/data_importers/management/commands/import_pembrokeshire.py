from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "PEM"
    addresses_name = "2024-05-02/2024-03-25T14:51:07.747895/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-25T14:51:07.747895/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
