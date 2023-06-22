from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRY"
    addresses_name = (
        "2023-06-29/2023-06-22T14:22:57.377959/Democracy_Club__29June2023.tsv"
    )
    stations_name = (
        "2023-06-29/2023-06-22T14:22:57.377959/Democracy_Club__29June2023.tsv"
    )
    elections = ["2023-06-29"]
    csv_delimiter = "\t"
