from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAB"
    addresses_name = (
        "2026-05-07/2026-02-17T12:44:19.717609/Democracy Club Polling Districts BDC.csv"
    )
    stations_name = (
        "2026-05-07/2026-02-17T12:44:19.717609/Democracy Club Polling Stations BDC.csv"
    )
    elections = ["2026-05-07"]
