from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MOL"
    addresses_name = "2026-12-10/2026-11-11T13:32:43.446271/Democracy_Club__10December2026 (Dorking Rural).tsv"
    stations_name = "2026-12-10/2026-11-11T13:32:43.446271/Democracy_Club__10December2026 (Dorking Rural).tsv"
    elections = ["2026-12-10"]
    csv_delimiter = "\t"
    csv_encoding = "latin_1"
