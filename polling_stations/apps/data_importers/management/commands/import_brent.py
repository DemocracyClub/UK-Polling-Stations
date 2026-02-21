from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BEN"
    addresses_name = "2026-05-07/2026-02-18T21:56:26.335831/Democracy Club Polling Districts 2026.csv"
    stations_name = "2026-05-07/2026-02-18T21:56:26.335831/Democracy Club Polling Polling Stations 2026.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
