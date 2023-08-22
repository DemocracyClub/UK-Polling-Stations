from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = (
        "2023-09-28/2023-08-22T15:33:12.407009/Democracry Club - Polling Districts.csv"
    )
    stations_name = (
        "2023-09-28/2023-08-22T15:33:12.407009/Democracry Club - Polling Stations.csv"
    )
    elections = ["2023-09-28"]
