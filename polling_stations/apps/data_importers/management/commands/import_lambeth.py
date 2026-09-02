from data_importers.management.commands import BaseFcsDemocracyClubImporter


class Command(BaseFcsDemocracyClubImporter):
    council_id = "LBH"
    addresses_name = "2026-10-08/2026-09-02T17:24:18.811795/snapshot.json"
    stations_name = "2026-10-08/2026-09-02T17:24:18.811795/snapshot.json"
    elections = ["2026-10-08"]
