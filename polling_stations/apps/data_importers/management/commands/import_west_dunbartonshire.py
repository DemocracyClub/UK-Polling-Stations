from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WDU"
    addresses_name = "2024-07-04/2024-06-06T10:20:42.600594/Eros_SQL_Output017.csv"
    stations_name = "2024-07-04/2024-06-06T10:20:42.600594/Eros_SQL_Output017.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "129058513",  # 53 CASTLEGATE AVENUE, DUMBARTON, G82 1AL
            "129048743",  # HIGHDYKES FARM, STIRLING ROAD, MILTON, DUMBARTON
        ]:
            return None

        if record.housepostcode in [
            # split
            "G81 5AW",
            "G60 5DP",
            "G81 3PY",
            "G82 3LE",
            "G82 4JS",
        ]:
            return None

        return super().address_record_to_dict(record)
