from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "THA"
    elections = ["2024-05-02"]
    fcs_election_id = 92

    def address_record_to_dict(self, record):
        if record["addressPostCode"] in [
            # split
            "CT10 3AD"
        ]:
            return None
        return super().address_record_to_dict(record)
