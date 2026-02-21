from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2026-05-07/2026-02-16T14:26:03.938575/Democracy Club - Idox_2026-02-16 14-12.csv"
    stations_name = "2026-05-07/2026-02-16T14:26:03.938575/Democracy Club - Idox_2026-02-16 14-12.csv"
    elections = ["2026-05-07"]
