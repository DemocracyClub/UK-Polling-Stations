from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RED"
    addresses_name = (
        "2024-07-04/2024-06-06T10:34:58.710969/Redditch Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-06T10:34:58.710969/Redditch Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]
