from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = (
        "2023-09-28/2023-08-23T18:36:37.245077/Democracry Club - Polling Districts.csv"
    )
    stations_name = (
        "2023-09-28/2023-08-23T18:36:37.245077/Democracry Club - Polling Stations.csv"
    )
    elections = ["2023-09-28"]
