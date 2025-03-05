from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = "2025-05-01/2025-03-05T14:07:34.619106/Democracy Club - Polling Districts 2025.csv"
    stations_name = "2025-05-01/2025-03-05T14:07:34.619106/Democracy Club - Polling Stations 2025.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
