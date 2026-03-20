from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAW"
    addresses_name = (
        "2026-05-07/2026-03-17T11:02:02.496814/Democracy_Club__07May2026SANDMBC.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T11:02:02.496814/Democracy_Club__07May2026SANDMBC.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
