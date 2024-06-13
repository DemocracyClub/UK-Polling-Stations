from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABD"
    addresses_name = (
        "2024-07-04/2024-06-07T15:42:14.722645/Eros_SQL_Output002 - Aberdeenshire.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-07T15:42:14.722645/Eros_SQL_Output002 - Aberdeenshire.csv"
    )
    elections = ["2024-07-04"]

    additional_report_councils = ["MRY"]
