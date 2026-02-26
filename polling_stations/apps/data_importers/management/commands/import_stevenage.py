from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = "2026-05-07/2026-02-20T14:19:29.496548/SBC Polling Districts.csv"
    stations_name = "2026-05-07/2026-02-20T14:19:29.496548/SBC Polling Stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
