from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAL"
    addresses_name = "2026-05-07/2026-03-05T14:13:38.499642/Democracy_Club__07May2026 -2026.03.05.tsv"
    stations_name = "2026-05-07/2026-03-05T14:13:38.499642/Democracy_Club__07May2026 -2026.03.05.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
