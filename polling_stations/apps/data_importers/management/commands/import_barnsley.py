from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNS"
    addresses_name = (
        "2023-05-04/2023-03-15T14:08:01.517673/Democracy_Club__04May2023(1).tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-15T14:08:01.517673/Democracy_Club__04May2023(1).tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
