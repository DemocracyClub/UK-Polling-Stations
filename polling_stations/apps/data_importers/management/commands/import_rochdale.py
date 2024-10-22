from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2024-10-31/2024-10-22T10:15:42.150160/Democracy_Club__31October2024.tsv"
    )
    stations_name = (
        "2024-10-31/2024-10-22T10:15:42.150160/Democracy_Club__31October2024.tsv"
    )
    elections = ["2024-10-31"]
    csv_delimiter = "\t"
