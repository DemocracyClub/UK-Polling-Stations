from data_importers.management.commands import BaseFcsDemocracyClubImporter


class Command(BaseFcsDemocracyClubImporter):
    council_id = "WND"
    addresses_name = "2026-05-06/2026-07-30T10:33:42.995231/snapshot.json"
    stations_name = "2026-05-06/2026-07-30T10:33:42.995231/snapshot.json"
    elections = ["2026-05-06"]
