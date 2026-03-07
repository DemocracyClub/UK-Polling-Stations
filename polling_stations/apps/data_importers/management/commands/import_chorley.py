from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CHO"
    addresses_name = "2026-05-07/2026-03-05T10:44:32.194903/Democracy Club - Idox_2026-03-05 10-36.csv"
    stations_name = "2026-05-07/2026-03-05T10:44:32.194903/Democracy Club - Idox_2026-03-05 10-36.csv"
    elections = ["2026-05-07"]
