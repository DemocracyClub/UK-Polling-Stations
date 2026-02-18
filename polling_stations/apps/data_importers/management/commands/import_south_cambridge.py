from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = (
        "2026-05-07/2026-02-18T11:00:52.688916/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-18T11:00:52.688916/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
