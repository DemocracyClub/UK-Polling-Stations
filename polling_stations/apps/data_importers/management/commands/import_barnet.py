from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = "2025-05-15/2025-04-24T10:25:36.116562/Democracy Club - Polling Districts WBE UTF-16LE.csv"
    stations_name = "2025-05-15/2025-04-24T10:25:36.116562/Democracy Club - Polling Stations WBE UTF-16LE.csv"
    elections = ["2025-05-15"]
    csv_encoding = "utf-16le"
