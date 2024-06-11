from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOX"
    addresses_name = "2024-07-04/2024-06-11T14:51:16.708318/Democracy_Club__04July2024 - Witney (1).tsv"
    stations_name = "2024-07-04/2024-06-11T14:51:16.708318/Democracy_Club__04July2024 - Witney (1).tsv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
