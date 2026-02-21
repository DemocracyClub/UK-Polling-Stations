from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2026-03-12/2026-02-17T11:10:16.984303/Democracy_Club__12March2026.tsv"
    )
    stations_name = (
        "2026-03-12/2026-02-17T11:10:16.984303/Democracy_Club__12March2026.tsv"
    )
    elections = ["2026-03-12"]
    csv_delimiter = "\t"
