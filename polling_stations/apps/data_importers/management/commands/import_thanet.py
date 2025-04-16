from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "THA"
    elections = ["2025-05-01"]
    fcs_election_id = 97

    def address_record_to_dict(self, record):
        uprn = str(record["addressUprn"]).lstrip("0").strip()

        if uprn in [
            "100061119615",  # PANDA CHINESE TAKE AWAY, 172 CANTERBURY ROAD, MARGATE
            "100062307971",  # 219 CANTERBURY ROAD, MARGATE
            "10013308944",  # 133A MINNIS ROAD, BIRCHINGTON
            "10095809065",  # 11B CHURCH STREET, MINSTER, RAMSGATE
            "100062281169",  # 10 RAMSGATE ROAD, BROADSTAIRS
            "100062305292",  # 3 DANE ROAD, MARGATE
            "100062094805",  # 10B DANE ROAD, MARGATE
            "100061120298",  # 49 COLLEGE ROAD, MARGATE
        ]:
            return None

        if record["addressPostCode"] in [
            # split
            "CT11 9RA",
            "CT10 3AD",
            # suspect
            "CT9 4AN",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Postcode correction from council for:
        # Cliftonville ( Outdoor) Bowls Club, St Georges Pavillion, Third Avenue, Margate CT9 2DW
        if record["id"] == 6866:
            record["addressPostCode"] = "CT9 2LN"

        return super().station_record_to_dict(record)
