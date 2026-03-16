from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "EDU"
    addresses_name = "2026-05-07/2026-03-16T14:16:57.693002/combined.csv"
    stations_name = "2026-05-07/2026-03-16T14:16:57.693002/combined.csv"
    elections = ["2026-05-07"]
