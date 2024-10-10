from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2024-11-14/2024-10-10T15:30:40.316715/Democracy_Club__14November2024.tsv"
    )
    stations_name = (
        "2024-11-14/2024-10-10T15:30:40.316715/Democracy_Club__14November2024.tsv"
    )
    elections = ["2024-11-14"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
