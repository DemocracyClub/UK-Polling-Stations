from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ABE"
    addresses_name = "2026-05-07/2026-03-09T16:25:32.686844/Democracy Club - Idox_2026-03-05 10-02.csv"
    stations_name = "2026-05-07/2026-03-09T16:25:32.686844/Democracy Club - Idox_2026-03-05 10-02.csv"
    elections = ["2026-05-07"]
