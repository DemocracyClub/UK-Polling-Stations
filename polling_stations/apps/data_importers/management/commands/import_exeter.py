from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = (
        "2024-05-02/2024-03-26T16:58:55.533065/Democracy_Club__02May2024-For Exeter.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-26T16:58:55.533065/Democracy_Club__02May2024-For Exeter.csv"
    )
    elections = ["2024-05-02"]
