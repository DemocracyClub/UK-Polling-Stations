from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HCK"
    addresses_name = (
        "2023-11-09/2023-10-12T10:40:53.760095/Democracy_Club__09November2023.CSV"
    )
    stations_name = (
        "2023-11-09/2023-10-12T10:40:53.760095/Democracy_Club__09November2023.CSV"
    )
    elections = ["2023-11-09"]
