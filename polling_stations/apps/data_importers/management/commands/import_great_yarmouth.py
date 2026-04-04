from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "GRY"
    addresses_name = "2026-05-07/2026-03-17T10:35:37.002013/Democracy Club - Idox_2026-03-17 10-31.csv"
    stations_name = "2026-05-07/2026-03-17T10:35:37.002013/Democracy Club - Idox_2026-03-17 10-31.csv"
    elections = ["2026-05-07"]

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
            "NR30 2LD",
            "NR31 6SY",
            "NR30 2DU",
            "NR31 9UP",
            "NR31 8AR",
            "NR30 5JU",
            "NR31 9PN",
            "NR30 2PY",
            "NR31 0AZ",
            "NR31 8BZ",
            "NR31 9NY",
            "NR31 9TY",
            "NR29 4SL",
            "NR31 9EJ",
            # suspect
            "NR31 9AQ",
            "NR29 4FF",
            "NR30 1TD",
            "NR31 6JN",
            "NR29 3PJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add missing postcode for: GORLESTON BAPTIST CHURCH, LOWESTOFT ROAD, GORLESTON
        if record.pollingstationnumber == "10":
            record = record._replace(pollingstationpostcode="NR31 6LY")

        # add missing postcode for: THURNE CHAPEL SCHOOLROOM, THURNE
        if record.pollingstationnumber == "38":
            record = record._replace(pollingstationpostcode="NR29 3AP")

        return super().station_record_to_dict(record)
