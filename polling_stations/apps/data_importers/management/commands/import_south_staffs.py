from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2026-12-17/2026-11-23T16:08:06.127888/Democracy_Club__17December2026FINAL.tsv"
    )
    stations_name = (
        "2026-12-17/2026-11-23T16:08:06.127888/Democracy_Club__17December2026FINAL.tsv"
    )
    elections = ["2026-12-17"]
    csv_delimiter = "\t"
