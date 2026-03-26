from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOT"
    addresses_name = (
        "2026-05-07/2026-03-17T12:17:24.284853/Democracy_Club__07May2026WBC.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T12:17:24.284853/Democracy_Club__07May2026WBC.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
