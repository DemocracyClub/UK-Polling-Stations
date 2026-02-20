from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "NTL"
    addresses_name = "2026-05-07/2026-02-20T15:54:09.716915/Democracy Club - Idox_2026-02-20 15-49.csv"
    stations_name = "2026-05-07/2026-02-20T15:54:09.716915/Democracy Club - Idox_2026-02-20 15-47.csv"
    elections = ["2026-05-07"]
