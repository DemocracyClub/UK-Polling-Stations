from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "GRT"
    addresses_name = "2026-05-07/2026-02-24T12:43:44.220496/Democracy Club - Idox_2026-02-24 12-26.csv"
    stations_name = "2026-05-07/2026-02-24T12:43:44.220496/Democracy Club - Idox_2026-02-24 12-26.csv"
    elections = ["2026-05-07"]
