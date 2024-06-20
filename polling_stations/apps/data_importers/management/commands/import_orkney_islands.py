from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ORK"
    addresses_name = (
        "2024-07-04/2024-06-20T14:58:29.571792/Orkney Eros_SQL_Output012.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-20T14:58:29.571792/Orkney Eros_SQL_Output012.csv"
    )
    elections = ["2024-07-04"]
