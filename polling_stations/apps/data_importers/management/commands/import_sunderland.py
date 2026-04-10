from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2026-05-07/2026-04-10T12:25:39.636850/2026 10 04 Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-10T12:25:39.636850/2026 10 04 Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
