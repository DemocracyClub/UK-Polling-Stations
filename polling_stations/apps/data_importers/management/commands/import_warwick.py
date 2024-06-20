from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WAW"
    addresses_name = (
        "2024-07-04/2024-06-20T10:43:28.610811/Democracy_Club__04July2024.CSV 1.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-20T10:43:28.610811/Democracy_Club__04July2024.CSV 1.csv"
    )
    elections = ["2024-07-04"]
