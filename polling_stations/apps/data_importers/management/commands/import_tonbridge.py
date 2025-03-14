from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TON"
    addresses_name = (
        "2025-05-01/2025-03-13T12:57:10.156992/Tonbridge & Malling data.csv"
    )
    stations_name = "2025-05-01/2025-03-13T12:57:10.156992/Tonbridge & Malling data.csv"
    elections = ["2025-05-01"]
