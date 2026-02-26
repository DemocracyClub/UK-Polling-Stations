from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAI"
    addresses_name = (
        "2026-05-07/2026-02-24T11:22:45.059332/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-24T11:22:45.059332/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
