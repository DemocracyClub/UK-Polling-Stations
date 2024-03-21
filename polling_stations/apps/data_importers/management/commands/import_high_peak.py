from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIG"
    addresses_name = (
        "2024-05-02/2024-03-21T13:43:41.849663/Democracy_Club__02May2024 (21).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T13:43:41.849663/Democracy_Club__02May2024 (21).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
