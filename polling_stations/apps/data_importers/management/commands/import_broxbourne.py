from data_importers.management.commands import Unknown


class Command(Unknown):
    council_id = "BRX"
    addresses_name = (
        "2025-05-01/2025-03-11T12:28:25.797277/POLLING STATIONS - 1.5.2025.csv"
    )
    stations_name = (
        "2025-05-01/2025-03-11T12:28:25.797277/POLLING STATIONS - 1.5.2025.csv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
