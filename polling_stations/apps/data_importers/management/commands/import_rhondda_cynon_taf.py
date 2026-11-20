from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = "2026-12-15/2026-11-20T09:23:31.554241/Democracy Club - Idox_2026-11-20 09-18.csv"
    stations_name = "2026-12-15/2026-11-20T09:23:31.554241/Democracy Club - Idox_2026-11-20 09-18.csv"
    elections = ["2026-12-15"]
