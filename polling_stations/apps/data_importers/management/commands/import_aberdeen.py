from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ABE"
    addresses_name = "2026-06-25/2026-05-18T10:10:09.390185/Democracy Club - Idox_2026-05-14 17-14 (1).csv"
    stations_name = "2026-06-25/2026-05-18T10:10:09.390185/Democracy Club - Idox_2026-05-14 17-14 (1).csv"
    elections = ["2026-06-25"]
