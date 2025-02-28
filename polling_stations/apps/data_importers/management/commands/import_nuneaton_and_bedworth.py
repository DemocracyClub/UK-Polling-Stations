from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NUN"
    addresses_name = (
        "2025-05-01/2025-02-28T13:08:50.423474/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-28T13:08:50.423474/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
