from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "TES"
    elections = ["2026-05-07"]
    fcs_election_id = 99

    def address_record_to_dict(self, record):
        if record.get(self.postcode_field).strip() in [
            # split
            "SP11 0HB"
        ]:
            return None
        return super().address_record_to_dict(record)
