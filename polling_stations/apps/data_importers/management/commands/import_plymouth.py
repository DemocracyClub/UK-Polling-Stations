from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PLY"
    addresses_name = (
        "2023-01-12/2022-12-14T10:55:16.177854/Democracy_Club__12January2023.tsv"
    )
    stations_name = (
        "2023-01-12/2022-12-14T10:55:16.177854/Democracy_Club__12January2023.tsv"
    )
    elections = ["2023-01-12"]
    csv_delimiter = "\t"
