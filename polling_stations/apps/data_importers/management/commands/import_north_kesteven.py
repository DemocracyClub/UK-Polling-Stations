from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2025-03-20/2025-02-25T13:31:51.166046/Democracy_Club__20March2025.tsv"
    )
    stations_name = (
        "2025-03-20/2025-02-25T13:31:51.166046/Democracy_Club__20March2025.tsv"
    )
    elections = ["2025-03-20"]
    csv_delimiter = "\t"
