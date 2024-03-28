from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ENF"
    addresses_name = (
        "2024-05-02/2024-03-28T13:33:06.828748/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-28T13:33:06.828748/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
