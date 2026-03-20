from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SCB"
    addresses_name = (
        "2026-05-07/2026-03-17T13:31:41.928875/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T13:31:41.928875/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
