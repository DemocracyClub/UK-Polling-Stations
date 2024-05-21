from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2024-06-13/2024-05-21T09:54:03.570856/Democracy_Club__13June2024.tsv"
    )
    stations_name = (
        "2024-06-13/2024-05-21T09:54:03.570856/Democracy_Club__13June2024.tsv"
    )
    elections = ["2024-06-13"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
