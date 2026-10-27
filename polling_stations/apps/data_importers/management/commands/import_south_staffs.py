from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2026-11-19/2026-10-27T15:16:59.730784/Democracy_Club__19November2026.tsv"
    )
    stations_name = (
        "2026-11-19/2026-10-27T15:16:59.730784/Democracy_Club__19November2026.tsv"
    )
    elections = ["2026-11-19"]
    csv_delimiter = "\t"
