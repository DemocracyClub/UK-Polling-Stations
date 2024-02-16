from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ISL"
    addresses_name = (
        "2024-05-02/2024-02-16T17:24:15.046914/Democracy_Club__02May2024.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-16T17:24:15.046914/Democracy_Club__02May2024.csv"
    )
    elections = ["2024-05-02"]
