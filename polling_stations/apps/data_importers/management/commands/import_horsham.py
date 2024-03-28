from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HOR"
    addresses_name = (
        "2024-05-02/2024-03-28T14:00:30.083404/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-28T14:00:30.083404/Democracy_Club__02May2024 (1).CSV"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
