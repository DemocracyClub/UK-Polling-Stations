from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "MSU"
    addresses_name = "2026-05-07/2026-02-17T12:44:03.194492/Democracy Club Polling Districts MSDC.csv"
    stations_name = (
        "2026-05-07/2026-02-17T12:44:03.194492/Democracy Club Polling Stations MSDC.csv"
    )
    elections = ["2026-05-07"]
