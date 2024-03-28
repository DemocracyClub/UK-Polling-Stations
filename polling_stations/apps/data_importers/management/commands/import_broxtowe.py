from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRT"
    addresses_name = "2024-05-02/2024-03-28T15:00:36.972423/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-28T15:00:36.972423/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
