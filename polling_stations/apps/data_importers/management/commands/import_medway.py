from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MDW"
    addresses_name = "2026-07-23/2026-07-22T16:04:15.115707/Democracy Club - Idox_2026-07-22 09-13.csv"
    stations_name = "2026-07-23/2026-07-22T16:04:15.115707/Democracy Club - Idox_2026-07-22 09-13.csv"
    elections = ["2026-07-23"]
