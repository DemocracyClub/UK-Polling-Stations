from data_importers.management.commands import BaseFcsDemocracyClubImporter


class Command(BaseFcsDemocracyClubImporter):
    council_id = "WND"
    addresses_name = "2026-05-06/2026-08-03T14:19:15.826594/snapshot.json"
    stations_name = "2026-05-06/2026-08-03T14:19:15.826594/snapshot.json"
    elections = ["2026-05-06"]
