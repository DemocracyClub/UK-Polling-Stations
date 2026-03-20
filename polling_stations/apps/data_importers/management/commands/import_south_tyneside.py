from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STY"
    addresses_name = (
        "2026-05-07/2026-03-11T10:30:53.150481/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-11T10:30:53.150481/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
