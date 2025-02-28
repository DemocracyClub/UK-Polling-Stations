from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = "2025-05-01/2025-02-28T12:20:51.689422/Democracy Club - Polling Districts 1 May 2025.csv"
    stations_name = "2025-05-01/2025-02-28T12:20:51.689422/Democracy Club - Polling Stations 1 May 2025.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
