from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRW"
    addresses_name = (
        "2024-05-02/2024-03-21T08:19:50.035033/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T08:19:50.035033/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
