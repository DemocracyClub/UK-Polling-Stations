from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "WDU"
    addresses_name = "2026-05-07/2026-03-16T14:15:07.857416/combined.csv"
    stations_name = "2026-05-07/2026-03-16T14:15:07.857416/combined.csv"
    elections = ["2026-05-07"]
