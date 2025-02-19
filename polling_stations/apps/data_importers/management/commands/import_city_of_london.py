from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LND"
    addresses_name = (
        "2025-03-20/2025-02-19T15:18:33.036157/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-03-20/2025-02-19T15:18:33.036157/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-03-20"]
    csv_encoding = "utf-16le"
