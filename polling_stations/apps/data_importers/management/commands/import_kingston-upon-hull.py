from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KHL"
    addresses_name = "2025-05-01/2025-03-27T11:43:28.234897/Democracy Club.tsv"
    stations_name = "2025-05-01/2025-03-27T11:43:28.234897/Democracy Club.tsv"
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
