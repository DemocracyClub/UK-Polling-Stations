from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "MRY"
    addresses_name = "2026-05-07/2026-03-16T11:58:21.052577/MRY_combined.csv"
    stations_name = "2026-05-07/2026-03-16T11:58:21.052577/MRY_combined.csv"
    elections = ["2026-05-07"]
