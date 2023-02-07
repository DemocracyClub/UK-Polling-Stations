from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAV"
    addresses_name = (
        "2023-05-04/2023-02-07T10:13:27.529328/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-07T10:13:27.529328/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
