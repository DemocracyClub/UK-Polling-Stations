from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = "2026-05-07/2026-02-16T14:24:39.850620/Democracy Club - Idox_2026-02-16 14-17.csv"
    stations_name = "2026-05-07/2026-02-16T14:24:39.850620/Democracy Club - Idox_2026-02-16 14-17.csv"
    elections = ["2026-05-07"]
