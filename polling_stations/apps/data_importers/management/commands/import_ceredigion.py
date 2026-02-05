from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = "2026-05-07/2026-02-05T14:21:50.846783/CEREDIGION - Democracy Club - Polling Districts_05.03.2026.csv"
    stations_name = "2026-05-07/2026-02-05T14:21:50.846783/CEREDIGION - Democracy Club - Polling Stations_05.03.2026.csv"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
