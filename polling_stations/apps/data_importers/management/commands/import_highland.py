from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = (
        "2024-04-11/2024-03-03T10:43:56.333233/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-04-11/2024-03-03T10:43:56.333233/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-04-11"]
    csv_encoding = "utf-16le"
