from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NTL"
    addresses_name = "2024-05-02/2024-03-18T17:05:04.301067/Eros_SQL_Output002.csv"
    stations_name = "2024-05-02/2024-03-18T17:05:04.301067/Eros_SQL_Output002.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200001853192",  # GLYNMEIRCH FARM, TYN Y PANT ROAD, PONTARDA\WE, SWANSEA
            "10009184465",  # CILGARN FARM, CWMAVON, PORT TALBOT
            "10009185877",  # 39 FAIRWOOD DRIVE, BAGLAN, PORT TALBOT
            "100100598790",  # 5 VERNON STREET, NEATH
            "10023946967",  # 134A SHELONE ROAD, BRITON FERRY
            "100100598607",  # 134 SHELONE ROAD, NEATH
            "10009183153",  # THE COTTAGE LANE FROM BURNSIDE TO GLAMORGAN FARM SCHOOL, NEATH
            "10023950856",  # 126B LONDON ROAD, NEATH
            "10009177319",  # MAES MELYN BUNGALOW, DRUMMAU ROAD, SKEWEN, NEATH
            "10023948013",  # THE BARN, TYCOCH FARM, RHYDDINGS, NEATH
            "10009183285",  # TYCOCH FARM, RHYDDINGS, NEATH
            "100190609132",  # 35B PENYWERN ROAD, NEATH
            "100100602551",  # FLAT 75 WINDSOR ROAD, NEATH
            "100101040310",  # NU TATU, 51-53 WINDSOR ROAD, NEATH
            "100190609132",  # 35B PENYWERN ROAD, NEATH
            "10009182091",  # 11A LONGFORD ROAD, NEATH
            "200001661738",  # MANOD 21 DRUMMAU ROAD, NEATH ABBEY
            "10009177450",  # FAIRYLAND HOUSE, FAIRYLAND ROAD, TONNA, NEATH
        ]:
            return None

        if record.housepostcode in [
            # splits
            "SA10 9DJ",
            "SA13 1JT",
            "SA10 6DE",
            "SA11 1TS",
            "SA12 8EP",
            "SA8 4TS",
            "SA11 3PW",
            "SA11 1TW",
            # looks wrong
            "SA9 2NW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Godrergraig Workingmens Club, Glanyrafon Road, Ystalyfera, SA9 2HA
        if record.pollingstationname == "Godrergraig Workingmens Club":
            record = record._replace(pollingstationpostcode="SA9 2DE")

        return super().station_record_to_dict(record)
