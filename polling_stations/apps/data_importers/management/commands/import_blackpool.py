from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPL"
    addresses_name = (
        "2024-05-02/2024-03-25T14:22:10.220217/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-25T14:22:10.220217/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
