from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2026-08-27/2026-07-14T12:13:31.238494/Democracy_Club__27August2026.tsv"
    )
    stations_name = (
        "2026-08-27/2026-07-14T12:13:31.238494/Democracy_Club__27August2026.tsv"
    )
    elections = ["2026-08-27"]
    csv_delimiter = "\t"
