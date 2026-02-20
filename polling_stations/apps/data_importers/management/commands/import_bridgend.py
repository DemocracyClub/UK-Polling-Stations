from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "BGE"
    addresses_name = "2026-05-07/2026-02-20T15:35:40.439319/Democracy Club - Idox_2026-02-20 15-33.csv"
    stations_name = "2026-05-07/2026-02-20T15:35:40.439319/Democracy Club - Idox_2026-02-18 09-45.csv"
    elections = ["2026-05-07"]
