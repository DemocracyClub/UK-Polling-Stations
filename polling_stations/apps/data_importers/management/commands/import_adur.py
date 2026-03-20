from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ADU"
    addresses_name = (
        "2026-05-07/2026-03-17T12:16:45.637360/Democracy_Club__07May2026ADC.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T12:16:45.637360/Democracy_Club__07May2026ADC.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
