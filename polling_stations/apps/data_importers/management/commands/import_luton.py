from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LUT"
    addresses_name = (
        "2023-05-04/2023-04-21T13:28:21.602825/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-21T13:28:21.602825/Democracy Club - Polling Stations.csv"
    )
    elections = ["2023-05-04"]
