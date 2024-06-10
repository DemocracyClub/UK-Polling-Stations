from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SFT"
    addresses_name = (
        "2024-07-04/2024-06-10T20:57:58.525616/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T20:57:58.525616/Democracy_Club__20June2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
