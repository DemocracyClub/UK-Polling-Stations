from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "OXO"
    elections = ["2026-05-07"]
    fcs_election_id = 18

    def address_record_to_dict(self, record):
        if record.get(self.postcode_field).strip() in [
            # split
            "OX3 0TX",
            "OX4 4UU",
            # suspect narrowboats
            "OX2 7AH",
        ]:
            return None
        return super().address_record_to_dict(record)
