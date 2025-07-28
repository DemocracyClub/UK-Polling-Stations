from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2025-08-14/2025-07-28T09:30:53.569803/Democracy_Club__14August2025.CSV"
    )
    stations_name = (
        "2025-08-14/2025-07-28T09:30:53.569803/Democracy_Club__14August2025.CSV"
    )
    elections = ["2025-08-14"]
