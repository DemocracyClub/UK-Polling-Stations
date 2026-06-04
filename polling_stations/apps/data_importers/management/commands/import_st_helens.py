from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = "2026-06-18/2026-06-04T11:21:46.194564/Democracy_Club__25June2026 - Updated (1).tsv"
    stations_name = "2026-06-18/2026-06-04T11:21:46.194564/Democracy_Club__25June2026 - Updated (1).tsv"
    elections = ["2026-06-18"]
    csv_delimiter = "\t"
