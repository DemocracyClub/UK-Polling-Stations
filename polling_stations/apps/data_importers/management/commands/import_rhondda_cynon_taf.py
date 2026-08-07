from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = "2026-09-03/2026-08-07T10:02:46.149348/Democracy Club - Idox_2026-08-07 09-55.csv"
    stations_name = "2026-09-03/2026-08-07T10:02:46.149348/Democracy Club - Idox_2026-08-07 09-55.csv"
    elections = ["2026-09-03"]
