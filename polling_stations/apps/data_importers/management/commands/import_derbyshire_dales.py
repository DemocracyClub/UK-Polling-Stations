from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DEB"
    addresses_name = "2025-05-01/2025-03-03T17:09:19.316607/Democracy Club Polling Districts County Council Election 1 May 2025.csv"
    stations_name = "2025-05-01/2025-03-03T17:09:19.316607/Democracy Club Polling Stations County Council Election 1 May 2025.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
