from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRA"
    addresses_name = (
        "2022-05-05/2022-04-08T14:35:11.201254/Democracy_Club__05May2022-7.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-08T14:35:11.201254/Democracy_Club__05May2022-7.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
