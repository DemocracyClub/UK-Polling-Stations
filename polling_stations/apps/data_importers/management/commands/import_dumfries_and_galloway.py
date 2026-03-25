from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = "2026-05-07/2026-03-25T13:10:50.926263/D&G Democracy Counts - Polling Districts 250326.csv"
    stations_name = "2026-05-07/2026-03-25T13:10:50.926263/D&G Democracy Counts - Polling Stations 250326.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
