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

    def station_record_to_dict(self, record):
        # address correction from council:
        # old: DALMUIR BARCLAY PARISH CHURCH, 21 DURBAN AVENUE, CLYDEBANK, G81 4JH
        # new: DALMUIR BARCLAY PARISH CHURCH, 20 DURBAN AVENUE, CLYDEBANK, G81 4JH
        if self.get_station_hash(record) in [
            "1-dalmuir-barclay-parish-church",
            "2-dalmuir-barclay-parish-church",
            "3-dalmuir-barclay-parish-church",
            "4-dalmuir-barclay-parish-church",
        ]:
            record = record._replace(pollingstationaddress_1="20 DURBAIN AVENUE")

        return super().station_record_to_dict(record)
