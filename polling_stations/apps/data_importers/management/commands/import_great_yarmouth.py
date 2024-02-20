from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRY"
    addresses_name = "2024-05-02/2024-02-20T16:34:00.297777/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-02-20T16:34:00.297777/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100091324017",  # HILLCREST, SCRATBY ROAD, SCRATBY, GREAT YARMOUTH
            "10023466441",  # ANDERSON HOUSE, SCRATBY ROAD, SCRATBY, GREAT YARMOUTH
            "100091564474",  # TOLLGATE BUNGALOW, NORWICH ROAD, WEST CAISTER, GREAT YARMOUTH
            "10012180501",  # THREE MILE HOUSE, WEST CAISTER, GREAT YARMOUTH
            "10023461782",  # HAVEN LEISURE LTD, SEASHORE HOLIDAY PARK, NORTH DRIVE, GREAT YARMOUTH
            "10023466830",  # CRUSADER BOATYARD, NORTH RIVER ROAD, GREAT YARMOUTH
            "10023467789",  # 20 SOUTH QUAY, GREAT YARMOUTH
            "200004442402",  # 62 ST. CATHERINES WAY, GORLESTON, GREAT YARMOUTH
            "100091318948",  # FIRST FLOOR FLAT 177 BELLS ROAD, GORLESTON, GREAT YARMOUTH
            "10012187666",  # 3 MAUTBY LANE, FILBY, GREAT YARMOUTH
            "100090841520",  # 20 GARRISON ROAD, GREAT YARMOUTH
            "10023465196",  # FLAT 1 76 HOWARD STREET SOUTH, GREAT YARMOUTH
            "10023465198",  # FLAT 3 76 HOWARD STREET SOUTH, GREAT YARMOUTH
            "10012180271",  # IRIS, RIVERSIDE, REPPS WITH BASTWICK, GREAT YARMOUTH
        ]:
            return None

        if record.housepostcode in [
            # split
            "NR31 9JF",
            "NR31 9PN",
            "NR29 4SL",
            "NR30 2PY",
            "NR31 0AZ",
            "NR31 8AR",
            "NR31 9NY",
            "NR31 9EJ",
            "NR30 2DU",
            "NR31 9TY",
            "NR31 9UP",
            "NR30 5JU",
            "NR31 6SY",
            "NR31 9AQ",  # WOODFARM COTTAGES, WOODFARM LANE, GORLESTON, GREAT YARMOUTH
            "NR31 8DH",  # ARCHES COURT, BECCLES ROAD, BRADWELL, GREAT YARMOUTH
            "NR29 4FF",  # REPPS MILL BARNS, MILL LANE, MARTHAM, GREAT YARMOUTH
            "NR30 4AW",  # JELLICOE ROAD, GREAT YARMOUTH
            "NR30 1TD",  # SCAREGAP COTTAGES, ACLE NEW ROAD, GREAT YARMOUTH
            "NR31 6JN",  # CLIFF PARK HOUSE, LOWESTOFT ROAD, GORLESTON, GREAT YARMOUTH
        ]:
            return None

        return super().address_record_to_dict(record)
