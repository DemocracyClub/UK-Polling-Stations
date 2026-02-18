from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2026-05-07/2026-02-18T09:56:09.315370/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-18T09:56:09.315370/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
