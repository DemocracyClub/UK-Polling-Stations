from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRW"
    addresses_name = (
        "2023-05-04/2023-03-21T16:26:51.918460/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-21T16:26:51.918460/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    # Nothing to correct, hurray!
