from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "STG"
    addresses_name = "2026-05-07/2026-03-20T15:51:13.206992/Democracy Club Stirling - Idox_2026-03-20 15-46.csv"
    stations_name = "2026-05-07/2026-03-20T15:51:13.206992/Democracy Club Stirling - Idox_2026-03-20 15-46.csv"
    elections = ["2026-05-07"]
