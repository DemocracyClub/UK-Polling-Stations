from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDG"
    addresses_name = (
        "2023-08-03/2023-07-03T09:24:49.364367/Democracy_Club__03August2023.tsv"
    )
    stations_name = (
        "2023-08-03/2023-07-03T09:24:49.364367/Democracy_Club__03August2023.tsv"
    )
    elections = ["2023-08-03"]
    csv_delimiter = "\t"
