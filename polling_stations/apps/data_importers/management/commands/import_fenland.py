from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FEN"
    addresses_name = "2025-05-01/2025-03-11T14:58:14.457984/Democracy Club FDC Polling Districts for May 2025.csv"
    stations_name = "2025-05-01/2025-03-11T14:58:14.457984/Democracy Club FDC Polling Stations for May 2025.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
