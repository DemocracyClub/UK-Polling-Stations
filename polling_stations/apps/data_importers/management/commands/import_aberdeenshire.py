from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ABD"
    addresses_name = "2026-05-07/2026-03-16T11:46:46.121836/ABD_combined_2.csv"
    stations_name = "2026-05-07/2026-03-16T11:46:46.121836/ABD_combined_2.csv"
    elections = ["2026-05-07"]
