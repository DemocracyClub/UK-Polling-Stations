from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NTL"
    addresses_name = "2024-07-04/2024-06-22T09:11:14.022359/ntl-combined.csv"
    stations_name = "2024-07-04/2024-06-22T09:11:14.022359/ntl-combined.csv"
    elections = ["2024-07-04"]
    not_in_ntl_stations = [
        "416-the-courthouse",
        "601-clydach-community-hall",
        "615-st-thomas-church",
        "617-st-stephens-church-hall",
        "413-garth-oap-centre",
        "417-bethania-baptist-church",
        "407-caerau-community-centre",
        "402-north-cornelly-community-centre",
        "610-talycopa-primary-school",
        "418-bryn-celyn-care-home",
        "611-llansamlet-community-centre",
        "604-glais-community-centre",
        "408-st-cynfelyns-church-hall",
        "412-llangynwyd-village-hall",
        "404-pyle-rugby-football-club",
        "608-community-area-the-pod",
        "403-1st-cornelly-scout-hall",
        "612-birchgrove-community-centre",
        "606-cwm-glas-primary-school",
        "405-pyle-life-centre",
        "406-talbot-community-centre",
        "414-salvation-army-hall",
        "614-mobile-station-opposite-13-parc-yr-helig-road",
        "603-graigfelen-hall",
        "613-birchgrove-community-centre",
        "605-waterfront-community-church",
        "415-st-michael-all-angels-church",
        "410-nantyffyllon-institute",
        "602-clydach-community-hall",
        "401-north-cornelly-community-centre",
        "409-noddfa-community-centre",
        "609-trallwn-community-centre",
        "411-cwmfelin-primary-school",
        "607-bonymaen-community-centre",
        "616-port-tennant-community-centre",
    ]

    def address_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_ntl_stations:
            return None
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
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
            ]
        ):
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
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_ntl_stations:
            return None
        # postcode correction for: Godrergraig Workingmens Club, Glanyrafon Road, Ystalyfera, SA9 2HA
        if record.pollingstationname == "Godrergraig Workingmens Club":
            record = record._replace(pollingstationpostcode="SA9 2DE")

        return super().station_record_to_dict(record)
