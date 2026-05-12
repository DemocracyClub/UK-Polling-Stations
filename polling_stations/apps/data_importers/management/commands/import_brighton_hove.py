from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2026-06-25/2026-05-12T08:38:13.140282/Democracy_Club__25June2026.CSV"
    )
    stations_name = (
        "2026-06-25/2026-05-12T08:38:13.140282/Democracy_Club__25June2026.CSV"
    )
    elections = ["2026-06-25"]
