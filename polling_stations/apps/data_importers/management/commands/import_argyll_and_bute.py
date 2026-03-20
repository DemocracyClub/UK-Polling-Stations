from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "AGB"
    addresses_name = "2026-05-07/2026-03-16T13:55:42.774579/combined.csv"
    stations_name = "2026-05-07/2026-03-16T13:55:42.774579/combined.csv"
    elections = ["2026-05-07"]
