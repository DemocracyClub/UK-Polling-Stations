from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CHT"
    addresses_name = "2026-05-07/2026-02-26T12:04:00.564616/Democracy Club - Idox_2026-02-24 10-38.csv"
    stations_name = "2026-05-07/2026-02-26T12:04:00.564616/Democracy Club - Idox_2026-02-24 10-38.csv"
    elections = ["2026-05-07"]
