from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HER"
    addresses_name = "2026-05-07/2025-12-11T14:43:48.145373/Democracy Club data.csv"
    stations_name = "2026-05-07/2025-12-11T14:43:48.145373/Democracy Club data.csv"
    elections = ["2026-05-07"]
