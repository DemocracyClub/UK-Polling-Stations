from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLF"
    addresses_name = (
        "2026-04-22/2026-03-17T11:00:56.422967/Democracy_Club__22April2026.tsv"
    )
    stations_name = (
        "2026-04-22/2026-03-17T11:00:56.422967/Democracy_Club__22April2026.tsv"
    )
    elections = ["2026-04-22"]
    csv_delimiter = "\t"
