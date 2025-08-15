from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = "2025-09-25/2025-08-15T17:03:14.048388/Democracy Club - Polling Districts W7 & W11.csv"
    stations_name = "2025-09-25/2025-08-15T17:03:14.048388/Democracy Club - Polling Stations W7 & W11.csv"
    elections = ["2025-09-25"]
    csv_encoding = "utf-16le"
