from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ABD"
    addresses_name = "2026-05-07/2026-03-09T16:26:40.637165/Democracy Club - Idox_2026-03-05 17-04.csv"
    stations_name = "2026-05-07/2026-03-09T16:26:40.637165/Democracy Club - Idox_2026-03-05 17-04.csv"
    elections = ["2026-05-07"]
