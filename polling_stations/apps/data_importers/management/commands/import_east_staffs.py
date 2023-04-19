from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "EST"
    addresses_name = (
        "2023-05-04/2023-04-13T15:18:20.766665/Democracy Club Polling Districts.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-13T15:18:20.766665/Democracy Club Polling Stations.csv"
    )
    elections = ["2023-05-04"]
