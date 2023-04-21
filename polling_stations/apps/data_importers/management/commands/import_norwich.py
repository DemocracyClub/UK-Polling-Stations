from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = (
        "2023-05-04/2023-04-21T13:20:24.756727/DC - Polling districts export.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-21T13:20:24.756727/DC - Polling stations export.csv"
    )
    elections = ["2023-05-04"]
