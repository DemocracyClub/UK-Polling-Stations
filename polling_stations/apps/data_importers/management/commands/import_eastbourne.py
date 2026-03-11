from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "EAS"
    addresses_name = "2026-05-07/2026-03-11T13:55:31.192407/Democracy Club - Idox_2026-03-11 13-45.csv"
    stations_name = "2026-05-07/2026-03-11T13:55:31.192407/Democracy Club - Idox_2026-03-11 13-45.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10010654823",  # FLAT 2 16A SILVERDALE ROAD, EASTBOURNE
                "10010662297",  # 141 WILLINGDON ROAD, EASTBOURNE
                "10010654824",  # FLAT 1 16A SILVERDALE ROAD, EASTBOURNE
                "10010661217",  # STAFF FLAT THE GRAND HOTEL KING EDWARDS PARADE, EASTBOURNE
                "10010661434",  # 1 HAMPDEN PARK DRIVE, EASTBOURNE
                "100061912921",  # SUMMERDOWN FARM COTTAGE, DOWNS VIEW LANE, EAST DEAN, EASTBOURNE
            ]
        ):
            return None

        if record.postcode in [
            # split
            "BN23 8JH",
            "BN20 8DP",
            # suspect
            "BN20 7BL",
            "BN21 2HD",
        ]:
            return None
        return super().address_record_to_dict(record)
