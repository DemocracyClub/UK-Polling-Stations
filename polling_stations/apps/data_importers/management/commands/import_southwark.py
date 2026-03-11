from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "SWK"
    elections = ["2026-05-07"]
    fcs_election_id = 58

    def address_record_to_dict(self, record):
        uprn = record.get(self.residential_uprn_field)

        if (
            uprn
            in [
                10097123458,  # FLAT 52 WALTER HOW COURT 840 OLD KENT ROAD, LONDON
                10097123449,  # FLAT 43 WALTER HOW COURT 840 OLD KENT ROAD, LONDON
                10096039125,  # 3A PLOUGH WAY, LONDON
                10009789022,  # BETRA COMMUNITY HALL, 28 RYEGATES, BRAYARDS ROAD ESTATE, LONDON
                10096875401,  # 79 THORNHILL HOUSE ILDERTON ROAD, LONDON
            ]
        ):
            return None
        if record.get(self.postcode_field).strip() in [
            # split
            "SE16 3RT",
            "SE5 0SY",
            "SE16 6AZ",
            "SE15 6BJ",
            # suspect:
            "SE24 9JQ",
        ]:
            return None
        return super().address_record_to_dict(record)
