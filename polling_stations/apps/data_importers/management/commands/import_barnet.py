from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = (
        "2023-05-04/2023-02-27T11:01:52.791010/Democracy Club_Polling Districts.csv"
    )
    stations_name = (
        "2023-05-04/2023-02-27T11:01:52.791010/Democracy Club_Polling Stations.csv"
    )
    elections = ["2023-05-04"]
