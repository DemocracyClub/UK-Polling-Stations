from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "LIC"
    addresses_name = "2026-05-07/2026-02-27T10:25:51.258710/Democracy Club - Idox_2026-02-27 10-24.csv"
    stations_name = "2026-05-07/2026-02-27T10:25:51.258710/Democracy Club - Idox_2026-02-27 10-24.csv"
    elections = ["2026-05-07"]
