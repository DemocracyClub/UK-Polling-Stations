from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2026-05-07/2026-02-23T09:23:31.641167/Democracy_Club__07May2026 (1).tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-23T09:23:31.641167/Democracy_Club__07May2026 (1).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
