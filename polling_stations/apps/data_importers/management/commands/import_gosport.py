from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "GOS"
    addresses_name = "2026-12-03/2026-10-27T15:04:32.190274/Democracy Club - Polling Districts - Gosport 03 12 2026.csv"
    stations_name = "2026-12-03/2026-10-27T15:04:32.190274/Democracy Club - Polling Stations  - Gosport 03 12 2026.csv"
    elections = ["2026-12-03"]
    csv_encoding = "utf-16le"
