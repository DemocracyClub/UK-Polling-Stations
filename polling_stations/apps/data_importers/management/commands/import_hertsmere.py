from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "HER"
    addresses_name = "2026-05-07/2026-04-16T16:06:49.796948/Democracy Club - Idox_2026-04-16 16-06.csv"
    stations_name = "2026-05-07/2026-04-16T16:06:49.796948/Democracy Club - Idox_2026-04-16 16-06.csv"
    elections = ["2026-05-07"]
