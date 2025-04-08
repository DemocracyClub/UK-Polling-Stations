from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEW"
    addresses_name = (
        "2025-05-01/2025-04-08T17:38:02.752651/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-08T17:38:02.752651/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    # Checked and no correction needed:
    # WARNING: Polling station The Edge Community Centre (10774) is in Stroud District Council (STO)
