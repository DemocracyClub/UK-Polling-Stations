from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BBD"
    addresses_name = (
        "2024-07-04/2024-06-18T10:36:16.375411/Democracy_Club__04July2024 (32).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-18T10:36:16.375411/Democracy_Club__04July2024 (32).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
