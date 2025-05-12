from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAS"
    addresses_name = (
        "2025-06-12/2025-05-12T16:42:47.513436/Democracy_Club__12June2025.tsv"
    )
    stations_name = (
        "2025-06-12/2025-05-12T16:42:47.513436/Democracy_Club__12June2025.tsv"
    )
    elections = ["2025-06-12"]
    csv_delimiter = "\t"
