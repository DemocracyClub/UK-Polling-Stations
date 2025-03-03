from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROS"
    addresses_name = (
        "2025-05-01/2025-03-03T14:45:03.997699/Democracy_Club__01May2025 (1).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-03T14:45:03.997699/Democracy_Club__01May2025 (1).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
