from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SHF"
    addresses_name = "2026-08-20/2026-07-20T16:41:29.719357/Democracy Club - Idox_2026-07-20 16-37.csv"
    stations_name = "2026-08-20/2026-07-20T16:41:29.719357/Democracy Club - Idox_2026-07-20 16-37.csv"
    elections = ["2026-08-20"]
