from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "DAR"
    addresses_name = "2024-05-02/2024-03-08T15:19:40.671473/Eros_SQL_Output002.csv"
    stations_name = "2024-05-02/2024-03-08T15:19:40.671473/Eros_SQL_Output002.csv"
    elections = ["2024-05-02"]
