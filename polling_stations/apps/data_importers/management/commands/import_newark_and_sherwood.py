from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEA"
    addresses_name = "2025-05-01/2025-03-17T15:39:24.857102/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-17T15:39:24.857102/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100031448570",  # 131 LIME GROVE, NEWARK
            "100032115885",  # HOLY TRINITY PRESBYTERY, BOUNDARY ROAD, NEWARK
            "100031446573",  # 2 HAWTON ROAD, NEWARK
            "100031458023",  # 74 STAUNTON ROAD, NEWARK
        ]:
            return None

        if record.housepostcode in [
            # split
            "NG24 5AB",
            "NG24 5BS",
            "NG24 5DB",
            "NG24 4BT",
            "NG21 9EE",
            "NG23 7ND",
            # suspect
            "NG22 9DY",
        ]:
            return None

        return super().address_record_to_dict(record)
