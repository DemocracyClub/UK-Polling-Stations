from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MDW"
    addresses_name = "2024-05-02/2024-03-21T14:40:57.823024/Eros_SQL_Output010.csv"
    stations_name = "2024-05-02/2024-03-21T14:40:57.823024/Eros_SQL_Output010.csv"
    elections = ["2024-05-02"]
