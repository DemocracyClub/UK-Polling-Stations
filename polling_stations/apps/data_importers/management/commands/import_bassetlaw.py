from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAE"
    addresses_name = (
        "2026-09-15/2026-08-20T10:53:29.048854/Democracy_Club__15September2026.tsv"
    )
    stations_name = (
        "2026-09-15/2026-08-20T10:53:29.048854/Democracy_Club__15September2026.tsv"
    )
    elections = ["2026-09-15"]
    csv_delimiter = "\t"
