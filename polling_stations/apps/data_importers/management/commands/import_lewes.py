from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "LEE"
    addresses_name = "2026-05-07/2026-03-17T15:52:41.578389/Democracy Club - Idox_2026-03-17 15-46.csv"
    stations_name = "2026-05-07/2026-03-17T15:52:41.578389/Democracy Club - Idox_2026-03-17 15-46.csv"
    elections = ["2026-05-07"]
