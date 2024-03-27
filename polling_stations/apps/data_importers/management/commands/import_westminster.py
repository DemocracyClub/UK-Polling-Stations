from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WSM"
    addresses_name = "2024-05-02/2024-03-27T14:42:03.748146/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-27T14:42:03.748146/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
