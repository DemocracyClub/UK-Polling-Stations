from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = "2026-05-07/2026-03-25T13:16:15.827019/D&G Democracy Counts - Polling Districts 250326.csv"
    stations_name = "2026-05-07/2026-03-25T13:16:15.827019/D&G Democracy Counts - Polling Stations 250326.csv"
    elections = ["2026-05-07"]
