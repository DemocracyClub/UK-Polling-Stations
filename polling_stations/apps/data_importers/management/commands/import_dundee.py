from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "DND"
    addresses_name = "2026-05-07/2026-02-23T10:35:14.409147/Democracy Club - Idox_2026-02-20 13-27.csv"
    stations_name = "2026-05-07/2026-02-23T10:35:14.409147/Democracy Club - Idox_2026-02-20 13-27.csv"
    elections = ["2026-05-07"]
