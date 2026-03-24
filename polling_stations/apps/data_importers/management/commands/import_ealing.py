from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAL"
    addresses_name = "2026-05-07/2026-03-24T14:55:25.345777/EC Democracy_Club__07May2026 Polling Station Lookup.tsv"
    stations_name = "2026-05-07/2026-03-24T14:55:25.345777/EC Democracy_Club__07May2026 Polling Station Lookup.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
