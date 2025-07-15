from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2025-08-14/2025-07-15T17:03:06.789754/Democracy_Club__24July2025 (1).CSV"
    )
    stations_name = (
        "2025-08-14/2025-07-15T17:03:06.789754/Democracy_Club__24July2025 (1).CSV"
    )
    elections = ["2025-08-14"]
