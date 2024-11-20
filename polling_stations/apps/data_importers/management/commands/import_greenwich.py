from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2024-12-19/2024-11-20T14:10:55.800536/Democracy_Club__19December2024.tsv"
    )
    stations_name = (
        "2024-12-19/2024-11-20T14:10:55.800536/Democracy_Club__19December2024.tsv"
    )
    elections = ["2024-12-19"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
