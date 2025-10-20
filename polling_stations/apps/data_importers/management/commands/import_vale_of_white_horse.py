from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "VAL"
    addresses_name = (
        "2025-11-13/2025-10-20T11:24:20.248349/Democracy_Club__13November2025.tsv"
    )
    stations_name = (
        "2025-11-13/2025-10-20T11:24:20.248349/Democracy_Club__13November2025.tsv"
    )
    elections = ["2025-11-13"]
    csv_delimiter = "\t"
