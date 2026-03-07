from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ORK"
    addresses_name = "2026-05-07/2026-03-05T12:17:43.857070/Democracy Club - Idox_2026-03-05 11-54.csv"
    stations_name = "2026-05-07/2026-03-05T12:17:43.857070/Democracy Club - Idox_2026-03-05 11-54.csv"
    elections = ["2026-05-07"]
