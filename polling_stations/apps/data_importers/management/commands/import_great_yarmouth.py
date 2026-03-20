from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "GRY"
    addresses_name = "2026-05-07/2026-03-17T10:35:37.002013/Democracy Club - Idox_2026-03-17 10-31.csv"
    stations_name = "2026-05-07/2026-03-17T10:35:37.002013/Democracy Club - Idox_2026-03-17 10-31.csv"
    elections = ["2026-05-07"]
