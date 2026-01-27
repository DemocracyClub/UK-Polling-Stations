from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ABE"
    addresses_name = (
        "2026-05-07/2026-01-27T16:52:41.436757/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2026-05-07/2026-01-27T16:52:41.436757/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
