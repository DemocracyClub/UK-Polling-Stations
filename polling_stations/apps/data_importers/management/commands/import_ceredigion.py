from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = (
        "2026-05-07/2025-11-21T13:13:01.523539/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2026-05-07/2025-11-21T13:13:01.523539/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
