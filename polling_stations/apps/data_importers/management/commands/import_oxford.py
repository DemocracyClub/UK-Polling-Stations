from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "OXO"
    addresses_name = "2024-05-02/2024-03-28T11:08:13.289353/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-28T11:08:13.289353/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
