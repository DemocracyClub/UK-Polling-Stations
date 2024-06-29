from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SPE"
    addresses_name = "2024-07-04/2024-06-29T10:37:45.305544/Eros_SQL_Output016.csv"
    stations_name = "2024-07-04/2024-06-29T10:37:45.305544/Eros_SQL_Output016.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "33012923",  # 259 FELTHAM HILL ROAD, ASHFORD
            "33012909",  # 257 FELTHAM HILL ROAD, ASHFORD
            "33012894",  # 255 FELTHAM HILL ROAD, ASHFORD
            "33035052",  # DERRYMORE, WRENS AVENUE, ASHFORD
            "33049394",  # VALDOR, WRENS AVENUE, ASHFORD
            "33049393",  # 54A WRENS AVENUE, ASHFORD
        ]:
            return None

        if record.housepostcode in [
            # split
            "TW15 1AG",
            "TW18 1HE",
            "TW15 3SH",
            # looks wrong
            "TW17 8SY",
            "TW18 1HD",
            "TW18 1QP",
            "TW18 1QW",
            "TW18 1QL",
            "TW18 1QN",
            "TW18 1HH",
            "TW18 1HG",
            "TW18 1HQ",
            "TW18 1HJ",
        ]:
            return None

        return super().address_record_to_dict(record)
