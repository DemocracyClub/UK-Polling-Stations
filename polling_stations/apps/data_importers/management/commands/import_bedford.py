from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BDF"
    addresses_name = (
        "2023-05-04/2023-03-09T13:02:35.083946/Democracy_Club__04May2023.csv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T13:02:35.083946/Democracy_Club__04May2023.csv"
    )
    elections = ["2023-05-04"]
