from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2026-03-05/2026-02-23T10:07:26.370972/Democracy_Club__07May2026 (3).tsv"
    )
    stations_name = (
        "2026-03-05/2026-02-23T10:07:26.370972/Democracy_Club__07May2026 (3).tsv"
    )
    elections = ["2026-03-05"]
    csv_delimiter = "\t"
