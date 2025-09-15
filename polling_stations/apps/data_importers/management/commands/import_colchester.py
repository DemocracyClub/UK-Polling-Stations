from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2025-10-23/2025-09-15T11:51:43.956849/Democracy_Club__23October2025.tsv"
    )
    stations_name = (
        "2025-10-23/2025-09-15T11:51:43.956849/Democracy_Club__23October2025.tsv"
    )
    elections = ["2025-10-23"]
    csv_delimiter = "\t"
