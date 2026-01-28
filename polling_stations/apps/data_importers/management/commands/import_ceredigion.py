from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = "2026-05-07/2026-01-28T11:46:49.953017/CEREDIGION - Polling Districts - DATA FILE.csv"
    stations_name = "2026-05-07/2026-01-28T11:46:49.953017/CEREDIGION - Data - Democracy Club - Polling Districts.csv"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
