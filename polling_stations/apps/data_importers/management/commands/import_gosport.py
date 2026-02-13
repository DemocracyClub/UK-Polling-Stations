from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "GOS"
    addresses_name = "2026-05-07/2026-02-13T14:03:56.860338/Democracy Club - Polling Districts - GOSPORT.csv"
    stations_name = "2026-05-07/2026-02-13T14:03:56.860338/Democracy Club - Polling Stations - GOSPORT.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
