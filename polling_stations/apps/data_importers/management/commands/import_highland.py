from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = (
        "2024-09-26/2024-08-29T13:52:40.782192/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-09-26/2024-08-29T13:52:40.782192/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-09-26"]
    csv_encoding = "utf-16le"
