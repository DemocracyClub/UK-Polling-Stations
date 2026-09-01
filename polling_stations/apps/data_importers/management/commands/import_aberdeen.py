from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABE"
    addresses_name = "2026-10-08/2026-09-01T16:05:03.429253/Democracy Club - Idox_2026-08-31 10-24.csv"
    stations_name = "2026-10-08/2026-09-01T16:05:03.429253/Democracy Club - Idox_2026-08-31 10-24.csv"
    elections = ["2026-10-08"]
