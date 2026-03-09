from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "MRY"
    addresses_name = "2026-05-07/2026-03-09T16:21:59.003966/Democracy Club - Idox_2026-03-05 09-30.csv"
    stations_name = "2026-05-07/2026-03-09T16:21:59.003966/Democracy Club - Idox_2026-03-05 09-30.csv"
    elections = ["2026-05-07"]
