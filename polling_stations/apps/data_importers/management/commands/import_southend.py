from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = (
        "2026-05-07/2026-03-19T11:32:49.463776/Democracy_Club__07May2026 (4).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-19T11:32:49.463776/Democracy_Club__07May2026 (4).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
