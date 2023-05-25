from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = (
        "2023-06-29/2023-05-25T11:35:14.762046/Democracy_Club__29June2023.CSV"
    )
    stations_name = (
        "2023-06-29/2023-05-25T11:35:14.762046/Democracy_Club__29June2023.CSV"
    )
    elections = ["2023-06-29"]
