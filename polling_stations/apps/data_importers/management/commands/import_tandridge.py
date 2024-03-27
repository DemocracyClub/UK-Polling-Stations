from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TAN"
    addresses_name = "2024-05-02/2024-03-27T10:39:00.996200/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-27T10:39:00.996200/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]
