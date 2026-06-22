from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRY"
    addresses_name = "2026-07-16/2026-06-22T12:37:11.119904/Democracy Club - Idox_2026-06-22 10-49.csv"
    stations_name = "2026-07-16/2026-06-22T12:37:11.119904/Democracy Club - Idox_2026-06-22 10-49.csv"
    elections = ["2026-07-16"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "100091564474",  # TOLLGATE BUNGALOW, NORWICH ROAD, WEST CAISTER, GREAT YARMOUTH
                "10012180501",  # THREE MILE HOUSE, WEST CAISTER, GREAT YARMOUTH
                "10023466830",  # CRUSADER BOATYARD, NORTH RIVER ROAD, GREAT YARMOUTH
                "10023467789",  # 20 SOUTH QUAY, GREAT YARMOUTH
                "200004442402",  # 62 ST. CATHERINES WAY, GORLESTON, GREAT YARMOUTH
                "10012187666",  # 3 MAUTBY LANE, FILBY, GREAT YARMOUTH
                "100090841520",  # 20 GARRISON ROAD, GREAT YARMOUTH
                "10023465196",  # FLAT 1 76 HOWARD STREET SOUTH, GREAT YARMOUTH
                "10023465198",  # FLAT 3 76 HOWARD STREET SOUTH, GREAT YARMOUTH
                "10012180271",  # IRIS, RIVERSIDE, REPPS WITH BASTWICK, GREAT YARMOUTH
                "100091616186",  # 220 BELLE AIRE HOLIDAY ESTATE BEACH ROAD, HEMSBY
                "10093370487",  # 59A BECCLES ROAD, GORLESTON, GREAT YARMOUTH
                "10012180864",  # 25 BACK CHAPEL LANE, GORLESTON, GREAT YARMOUTH
            ]
        ):
            return None

        if record.postcode in [
            # split
            "NR29 4SL",
            "NR30 2DU",
            "NR30 2PY",
            "NR30 5JU",
            "NR31 0AZ",
            "NR31 6SY",
            "NR31 8AR",
            "NR31 8BZ",
            "NR31 9EJ",
            "NR31 9NY",
            "NR31 9PN",
            "NR31 9TY",
            "NR31 9UP",
            # suspect
            "NR29 3PJ",
            "NR29 4FF",
            "NR30 1TD",
            "NR31 6JN",
            "NR31 9AQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add missing postcode for: THURNE CHAPEL SCHOOLROOM, THURNE
        if self.get_station_hash(record) == "41-thurne-chapel-schoolroom":
            record = record._replace(pollingstationpostcode="NR29 3AP")

        return super().station_record_to_dict(record)
