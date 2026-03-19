from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "EDH"
    addresses_name = "2026-05-07/2026-03-19T16:12:33.586653/Democracy Club - Idox_2026-03-17 11-16.csv"
    stations_name = "2026-05-07/2026-03-19T16:12:33.586653/Democracy Club - Idox_2026-03-17 11-16.csv"
    elections = ["2026-05-07"]
