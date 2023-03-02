from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRD"
    addresses_name = (
        "2023-05-04/2023-03-02T16:21:41.882014/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-02T16:21:41.882014/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
