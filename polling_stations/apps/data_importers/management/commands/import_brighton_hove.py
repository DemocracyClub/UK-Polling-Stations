from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2024-01-11/2023-12-08T17:22:51.514333/Democracy_Club__11January2024.tsv"
    )
    stations_name = (
        "2024-01-11/2023-12-08T17:22:51.514333/Democracy_Club__11January2024.tsv"
    )
    elections = ["2024-01-11"]
    csv_delimiter = "\t"
