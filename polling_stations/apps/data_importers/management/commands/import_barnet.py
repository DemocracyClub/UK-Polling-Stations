from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = (
        "2026-05-07/2026-03-20T15:16:34.415654/Democracy Club - Polling Districs.csv"
    )
    stations_name = (
        "2026-05-07/2026-03-20T15:16:34.415654/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
