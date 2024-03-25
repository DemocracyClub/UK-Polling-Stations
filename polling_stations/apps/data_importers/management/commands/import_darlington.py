from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAL"
    addresses_name = (
        "2024-05-02/2024-03-25T17:20:18.000995/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-25T17:20:18.000995/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
