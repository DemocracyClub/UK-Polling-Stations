from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAV"
    addresses_name = (
        "2023-08-10/2023-07-17T09:13:19.161631/Democracy_Club__10August2023.tsv"
    )
    stations_name = (
        "2023-08-10/2023-07-17T09:13:19.161631/Democracy_Club__10August2023.tsv"
    )
    elections = ["2023-08-10"]
    csv_delimiter = "\t"
