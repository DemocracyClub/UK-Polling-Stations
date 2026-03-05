from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ELM"
    addresses_name = "2026-05-07/2026-03-05T18:03:47.545023/Democracy Club - Idox_2026-03-03 21-35.csv"
    stations_name = "2026-05-07/2026-03-05T18:03:47.545023/Democracy Club - Idox_2026-03-03 21-35.csv"
    elections = ["2026-05-07"]
