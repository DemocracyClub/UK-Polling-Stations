from data_importers.management.commands import BaseFcsDemocracyClubImporter


class Command(BaseFcsDemocracyClubImporter):
    council_id = "WND"
    addresses_name = "2024-07-03/2026-07-30T08:32:50.141402/snapshot2.json"
    stations_name = "2024-07-03/2026-07-30T08:32:50.141402/snapshot2.json"
    elections = ["2024-07-03"]
