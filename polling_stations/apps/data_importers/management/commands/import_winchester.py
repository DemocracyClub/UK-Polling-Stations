from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = (
        "2023-05-04/2023-03-16T11:44:33.067222/Democracy_Club__04May2023 - 15 wards.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-16T11:44:33.067222/Democracy_Club__04May2023 - 15 wards.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
