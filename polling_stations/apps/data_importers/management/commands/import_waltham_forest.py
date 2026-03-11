from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "WFT"
    elections = ["2026-05-07"]
    fcs_election_id = 29

    def address_record_to_dict(self, record):
        uprn = record.get(self.residential_uprn_field)

        if (
            uprn
            in [
                100022961813,  # 596A HIGH ROAD LEYTONSTONE, LONDON
                200001416768,  # 24B COURTENAY ROAD, LEYTONSTONE
                10024418210,  # 5A ELY ROAD, LONDON
                100022597435,  # VILLA NURSES HOME WHIPPS CROSS HOSPITAL WHIPPS CROSS ROAD, LEYTONSTONE
                100022985629,  # 2 ORFORD ROAD, LONDON
            ]
        ):
            return None
        if record.get(self.postcode_field).strip() in [
            # split
            "E4 9DP",
            "E17 5JY",
            "E11 3DT",
            "E17 3NL",
            "E17 3EQ",
            "E17 7EA",
            "E11 3EA",
            "E17 3DU",
            "E17 4ED",
            # suspect:
            "E11 1LJ",
        ]:
            return None
        return super().address_record_to_dict(record)
