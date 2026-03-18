from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "NLK"
    addresses_name = "2026-05-07/2026-03-18T09:20:01.974806/Democracy Club - Idox_2026-03-17 14-28.csv"
    stations_name = "2026-05-07/2026-03-18T09:20:01.974806/Democracy Club - Idox_2026-03-17 14-28.csv"
    elections = ["2026-05-07"]
