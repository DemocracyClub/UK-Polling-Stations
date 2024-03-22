from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWL"
    addresses_name = (
        "2024-05-02/2024-03-22T14:00:13.485984/SWALE_Eros_SQL_Output001.csv"
    )
    stations_name = "2024-05-02/2024-03-22T14:00:13.485984/SWALE_Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
