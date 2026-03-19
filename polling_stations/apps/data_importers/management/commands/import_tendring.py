from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = "2026-05-07/2026-03-19T10:47:08.499497/Democracy Club - Polling Districts 2026.csv"
    stations_name = "2026-05-07/2026-03-19T10:47:08.499497/Democracy Club - Polling Stations 2026.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
