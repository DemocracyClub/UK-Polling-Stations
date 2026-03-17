from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SUR"
    addresses_name = (
        "2026-05-07/2026-03-17T15:49:04.184883/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T15:49:04.184883/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
