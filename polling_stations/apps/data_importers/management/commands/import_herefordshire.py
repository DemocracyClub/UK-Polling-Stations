from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HEF"
    addresses_name = "2024-11-07/2024-10-11T14:07:13.994161/Democracy Club data - Bishops Frome & Cradley.csv"
    stations_name = "2024-11-07/2024-10-11T14:07:13.994161/Democracy Club data - Bishops Frome & Cradley.csv"
    elections = ["2024-11-07"]
