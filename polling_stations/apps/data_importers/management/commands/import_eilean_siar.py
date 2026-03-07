from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ELS"
    addresses_name = "2026-05-07/2026-03-01T07:46:42.121381/Democracy Club - Polling Districts WI.csv"
    stations_name = (
        "2026-05-07/2026-03-01T07:46:42.121381/Democracy Club - Polling Stations WI.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
