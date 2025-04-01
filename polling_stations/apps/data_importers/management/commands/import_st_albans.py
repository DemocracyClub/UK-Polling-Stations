from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAL"
    addresses_name = "2025-05-01/2025-04-01T10:09:01.084097/Democracy_Club__01May2025_Redbourn by election.tsv"
    stations_name = "2025-05-01/2025-04-01T10:09:01.084097/Democracy_Club__01May2025_Redbourn by election.tsv"
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
