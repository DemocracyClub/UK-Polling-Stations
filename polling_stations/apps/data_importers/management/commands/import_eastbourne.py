from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "EAS"
    addresses_name = "2026-05-07/2026-03-11T13:55:31.192407/Democracy Club - Idox_2026-03-11 13-45.csv"
    stations_name = "2026-05-07/2026-03-11T13:55:31.192407/Democracy Club - Idox_2026-03-11 13-45.csv"
    elections = ["2026-05-07"]
