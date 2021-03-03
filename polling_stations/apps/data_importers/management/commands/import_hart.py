from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAT"
    addresses_name = (
        "2021-03-03T10:59:35.556539/Hart District Democracy_Club_06May2021.tsv"
    )
    stations_name = (
        "2021-03-03T10:59:35.556539/Hart District Democracy_Club_06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
