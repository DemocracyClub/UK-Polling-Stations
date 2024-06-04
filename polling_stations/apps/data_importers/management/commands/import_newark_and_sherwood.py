from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEA"
    addresses_name = "2024-07-04/2024-06-04T11:45:51.882314/Eros_SQL_Output012.csv"
    stations_name = "2024-07-04/2024-06-04T11:45:51.882314/Eros_SQL_Output012.csv"
    elections = ["2024-07-04"]

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
            "NG24 4JW",
            "NG24 4BT",
            "NG24 3PA",
            "NG25 0LQ",
            "NG24 5BS",
            "NG21 9EE",
            # suspect
            "NG24 4RZ",
            "NG22 9DY",
        ]:
            return None

        return super().address_record_to_dict(record)
