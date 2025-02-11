from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2025-02-20/2025-02-11T10:40:31.821365/Democracy_Club__20February2025.tsv"
    )
    stations_name = (
        "2025-02-20/2025-02-11T10:40:31.821365/Democracy_Club__20February2025.tsv"
    )
    elections = ["2025-02-20"]
    csv_delimiter = "\t"
