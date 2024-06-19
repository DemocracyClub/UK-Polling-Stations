from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIL"
    addresses_name = (
        "2024-07-04/2024-06-19T09:41:43.843988/Democracy_Club__04July2024.tsvRNP.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-19T09:41:43.843988/Democracy_Club__04July2024.tsvRNP.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
