from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "PKN"
    addresses_name = "2026-05-07/2026-02-26T11:26:10.906252/Democracy Club - Idox_2026-02-26 10-31.csv"
    stations_name = "2026-05-07/2026-02-26T11:26:10.906252/Democracy Club - Idox_2026-02-26 10-31.csv"
    elections = ["2026-05-07"]
