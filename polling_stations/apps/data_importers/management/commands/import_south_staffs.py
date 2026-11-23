from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2026-12-17/2026-11-23T10:25:42.708814/Democracy_Club__17December2026.tsv"
    )
    stations_name = (
        "2026-12-17/2026-11-23T10:25:42.708814/Democracy_Club__17December2026.tsv"
    )
    elections = ["2026-12-17"]
    csv_delimiter = "\t"
