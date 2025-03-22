from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NLN"
    addresses_name = "2025-05-01/2025-03-11T17:08:37.404782/Polling Stations-North Lincolnshire Council.csv"
    stations_name = "2025-05-01/2025-03-11T17:08:37.404782/Polling Stations-North Lincolnshire Council.csv"
    elections = ["2025-05-01"]
