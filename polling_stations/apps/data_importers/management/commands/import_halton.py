from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAL"
    addresses_name = "2026-05-07/2026-03-10T13:38:01.597846/Halton Borough Council Democracy_Club__07May2026.tsv"
    stations_name = "2026-05-07/2026-03-10T13:38:01.597846/Halton Borough Council Democracy_Club__07May2026.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
