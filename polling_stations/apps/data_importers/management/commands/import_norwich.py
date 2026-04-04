from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = (
        "2026-05-07/2026-03-31T15:27:14.069048/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2026-05-07/2026-03-31T15:27:14.069048/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
