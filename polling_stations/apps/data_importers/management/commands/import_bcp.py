from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = (
        "2026-11-05/2026-09-24T15:50:01.228864/Democracy_Club__05November2026.tsv"
    )
    stations_name = (
        "2026-11-05/2026-09-24T15:50:01.228864/Democracy_Club__05November2026.tsv"
    )
    elections = ["2026-11-05"]
    csv_delimiter = "\t"
