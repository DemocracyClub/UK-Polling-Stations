from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2026-05-07/2026-03-06T14:11:59.587542/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-06T14:11:59.587542/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
