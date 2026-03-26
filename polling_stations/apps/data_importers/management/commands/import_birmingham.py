from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "BIR"
    addresses_name = "2026-05-07/2026-03-16T17:42:35.689839/Democracy Club - Idox_2026-03-16 17-34.csv"
    stations_name = "2026-05-07/2026-03-16T17:42:35.689839/Democracy Club - Idox_2026-03-16 17-34.csv"
    elections = ["2026-05-07"]
