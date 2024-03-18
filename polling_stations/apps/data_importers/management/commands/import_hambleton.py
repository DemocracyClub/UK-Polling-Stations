from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAE"
    addresses_name = (
        "2024-05-02/2024-03-15T16:16:28.044890/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-15T16:16:28.044890/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
