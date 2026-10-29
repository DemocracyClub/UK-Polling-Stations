from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2026-11-26/2026-10-29T08:49:09.599577/Democracy_Club__26November2026.tsv"
    )
    stations_name = (
        "2026-11-26/2026-10-29T08:49:09.599577/Democracy_Club__26November2026.tsv"
    )
    elections = ["2026-11-26"]
    csv_delimiter = "\t"
