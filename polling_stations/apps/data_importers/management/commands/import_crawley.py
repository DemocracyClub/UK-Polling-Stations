from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRW"
    addresses_name = (
        "2026-05-07/2026-02-26T11:10:58.501372/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-26T11:10:58.501372/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
