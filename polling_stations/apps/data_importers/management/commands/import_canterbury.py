from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAT"
    addresses_name = (
        "2025-11-13/2025-10-22T13:29:07.725464/Democracy_Club__13November2025.CSV"
    )
    stations_name = (
        "2025-11-13/2025-10-22T13:29:07.725464/Democracy_Club__13November2025.CSV"
    )
    elections = ["2025-11-13"]
