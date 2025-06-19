from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2025-06-26/2025-06-19T20:52:32.985120/Democracy_Club__26June2025.tsv"
    )
    stations_name = (
        "2025-06-26/2025-06-19T20:52:32.985120/Democracy_Club__26June2025.tsv"
    )
    elections = ["2025-06-26"]
    csv_delimiter = "\t"
