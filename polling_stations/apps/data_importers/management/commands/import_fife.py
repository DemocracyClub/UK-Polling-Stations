from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FIF"
    addresses_name = (
        "2026-05-07/2026-02-18T15:06:41.753682/Democracy Club - Polling District 2.csv"
    )
    stations_name = (
        "2026-05-07/2026-02-18T15:06:41.753682/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
