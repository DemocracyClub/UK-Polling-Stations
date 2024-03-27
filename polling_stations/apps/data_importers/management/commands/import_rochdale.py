from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2024-05-02/2024-03-27T10:00:00.966473/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-27T10:00:00.966473/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
