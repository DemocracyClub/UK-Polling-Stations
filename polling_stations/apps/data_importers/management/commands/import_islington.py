from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ISL"
    addresses_name = (
        "2024-11-28/2024-10-30T14:47:36.249110/Democracy_Club__28November2024.CSV"
    )
    stations_name = (
        "2024-11-28/2024-10-30T14:47:36.249110/Democracy_Club__28November2024.CSV"
    )
    elections = ["2024-11-28"]
