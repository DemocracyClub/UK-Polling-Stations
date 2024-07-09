from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = (
        "2024-07-18/2024-07-09T09:08:42.898950/Democracy_Club__18July2024.tsv"
    )
    stations_name = (
        "2024-07-18/2024-07-09T09:08:42.898950/Democracy_Club__18July2024.tsv"
    )
    elections = ["2024-07-18"]
    csv_delimiter = "\t"
