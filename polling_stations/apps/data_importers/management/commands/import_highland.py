from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = (
        "2025-06-19/2025-05-16T13:13:53.339724/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-06-19/2025-05-16T13:13:53.339724/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-06-19"]
    csv_encoding = "utf-16le"
