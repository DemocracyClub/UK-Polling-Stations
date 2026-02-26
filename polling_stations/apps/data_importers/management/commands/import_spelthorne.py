from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "SPE"
    addresses_name = "2026-05-07/2026-02-26T11:34:38.261833/Democracy Club - Idox_2026-02-25 16-08.csv"
    stations_name = "2026-05-07/2026-02-26T11:34:38.261833/Democracy Club - Idox_2026-02-25 16-08.csv"
    elections = ["2026-05-07"]
