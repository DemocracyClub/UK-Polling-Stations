from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "RFW"
    addresses_name = "2026-05-07/2026-02-19T12:45:14.327541/Democracy Club - Polling District (Ren).csv"
    stations_name = "2026-05-07/2026-02-19T12:45:14.327541/Democracy Club - Polling Stations (Ren).csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
