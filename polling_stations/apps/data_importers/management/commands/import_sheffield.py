from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "SHF"
    addresses_name = "2026-05-07/2026-03-05T21:25:47.332823/Democracy Club - Idox_2026-03-05 17-45.csv"
    stations_name = "2026-05-07/2026-03-05T21:25:47.332823/Democracy Club - Idox_2026-03-05 17-45.csv"
    elections = ["2026-05-07"]
