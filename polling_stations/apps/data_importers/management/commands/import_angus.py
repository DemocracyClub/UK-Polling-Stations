from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ANS"
    addresses_name = "2026-05-07/2026-02-26T11:28:34.228815/Democracy Club - Idox_2026-02-26 10-26.csv"
    stations_name = "2026-05-07/2026-02-26T11:28:34.228815/Democracy Club - Idox_2026-02-26 10-26.csv"
    elections = ["2026-05-07"]
