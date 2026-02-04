from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2026-02-26/2026-02-04T14:12:40.743599/Democracy_Club__26February2026.tsv"
    )
    stations_name = (
        "2026-02-26/2026-02-04T14:12:40.743599/Democracy_Club__26February2026.tsv"
    )
    elections = ["2026-02-26"]
    csv_delimiter = "\t"
