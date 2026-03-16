from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "TAN"
    addresses_name = "2026-05-07/2026-03-16T13:01:38.577321/Democracy Club - Idox_2026-03-16 12-02.csv"
    stations_name = "2026-05-07/2026-03-16T13:01:38.577321/Democracy Club - Idox_2026-03-16 12-02.csv"
    elections = ["2026-05-07"]
