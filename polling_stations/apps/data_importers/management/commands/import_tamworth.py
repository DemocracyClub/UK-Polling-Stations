from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = (
        "2026-03-05/2026-02-26T15:42:16.527435/Democracy_Club__05March2026.tsv"
    )
    stations_name = (
        "2026-03-05/2026-02-26T15:42:16.527435/Democracy_Club__05March2026.tsv"
    )
    elections = ["2026-03-05"]
    csv_delimiter = "\t"
