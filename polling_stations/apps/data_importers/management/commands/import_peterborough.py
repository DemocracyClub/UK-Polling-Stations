from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PTE"
    addresses_name = (
        "2026-05-07/2026-03-17T13:30:43.807486/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T13:30:43.807486/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
