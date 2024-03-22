from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2024-05-02/2024-03-22T10:01:04.870722/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-22T10:01:04.870722/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]
