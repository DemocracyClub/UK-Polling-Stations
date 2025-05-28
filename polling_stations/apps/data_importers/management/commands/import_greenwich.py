from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2025-06-26/2025-05-28T15:20:53.146701/Democracy_Club__26June2025.tsv"
    )
    stations_name = (
        "2025-06-26/2025-05-28T15:20:53.146701/Democracy_Club__26June2025.tsv"
    )
    elections = ["2025-06-26"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
