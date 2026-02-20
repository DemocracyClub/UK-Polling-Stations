from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "MTY"
    addresses_name = "2026-05-07/2026-02-20T15:14:47.599472/Democracy Club - Idox_2026-02-20 15-05.csv"
    stations_name = "2026-05-07/2026-02-20T15:14:47.599472/Democracy Club - Idox_2026-02-20 15-05.csv"
    elections = ["2026-05-07"]
