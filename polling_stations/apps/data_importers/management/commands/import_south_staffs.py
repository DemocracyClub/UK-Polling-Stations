from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2023-05-04/2023-04-03T14:58:59.354138/Democracy_Club__04May2023v.2.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-03T14:58:59.354138/Democracy_Club__04May2023v.2.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
