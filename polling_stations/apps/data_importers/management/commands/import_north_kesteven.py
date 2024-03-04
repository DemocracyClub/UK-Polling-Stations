from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2024-05-02/2024-03-04T16:20:03.322219/Democracy_Club__02May2024 (8).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-04T16:20:03.322219/Democracy_Club__02May2024 (8).tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
