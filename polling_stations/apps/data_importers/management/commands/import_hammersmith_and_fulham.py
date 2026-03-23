from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "HMF"
    addresses_name = "2026-05-07/2026-03-23T16:29:14.716605/Democracy Club - Idox_2026-03-23 16-25.csv"
    stations_name = "2026-05-07/2026-03-23T16:29:14.716605/Democracy Club - Idox_2026-03-23 16-25.csv"
    elections = ["2026-05-07"]
