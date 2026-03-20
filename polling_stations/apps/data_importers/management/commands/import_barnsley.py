from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNS"
    addresses_name = (
        "2026-05-07/2026-03-09T15:25:57.168402/Democracy Club - polling districts.csv"
    )
    stations_name = (
        "2026-05-07/2026-03-09T15:25:57.168402/Democracy Club - polling stations.csv"
    )
    elections = ["2026-05-07"]
