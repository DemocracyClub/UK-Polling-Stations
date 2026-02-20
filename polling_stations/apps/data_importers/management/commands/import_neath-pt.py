from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "NTL"
    addresses_name = "2026-05-07/2026-02-23T12:29:03.704038/NTL_combined.csv"
    stations_name = "2026-05-07/2026-02-23T12:29:03.704038/NTL_combined.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10009185877",  # 39 FAIRWOOD DRIVE, BAGLAN, PORT TALBOT
                "100100598790",  # 5 VERNON STREET, NEATH
                "10023946967",  # 134A SHELONE ROAD, BRITON FERRY
                "100100598607",  # 134 SHELONE ROAD, NEATH
                "10009183153",  # THE COTTAGE LANE FROM BURNSIDE TO GLAMORGAN FARM SCHOOL, NEATH
                "10023950856",  # 126B LONDON ROAD, NEATH
                "10009177319",  # MAES MELYN BUNGALOW, DRUMMAU ROAD, SKEWEN, NEATH
                "10023948013",  # THE BARN, TYCOCH FARM, RHYDDINGS, NEATH
                "10009182091",  # 11A LONGFORD ROAD, NEATH
                "200001661738",  # MANOD 21 DRUMMAU ROAD, NEATH ABBEY
                "10009183439",  # CEFN Y GELLI, CLYNE, NEATH
                "100100991905",  # BROOKLYN, TONMAWR ROAD, PONTRHYDYFEN, PORT TALBOT
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "SA11 1TW",
            "SA11 1TS",
            "SA13 1JT",
            "SA12 8EP",
            "SA10 6DE",
            "SA11 3PW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Godrergraig Workingmens Club, Glanyrafon Road, Ystalyfera, SA9 2HA
        if self.get_station_hash(record) == "826-godrergraig-workingmens-club":
            record = record._replace(pollingstationpostcode="SA9 2DE")

        # postcode mismatches pending council reply:
        # # 'Aberavon Community Resource Centre (NSA), Michna Street, Port Talbot, SA12 6UH' (id: 3)
        # if record.pollingvenueid == "3":
        #     record = record._replace(pollingstationpostcode="SA12 6LR")

        # # 'Baglan Community Centre, Hawthorn Avenue, Baglan, SA12 8PG' (id: 11)
        # if record.pollingvenueid == "11":
        #     record = record._replace(pollingstationpostcode="SA12 8PH")

        # # 'Hengwrt Community Sports Centre, Llansawel Crescent, Briton Ferry, Neath, SA11 2UW' (id: 15)
        # if record.pollingvenueid == "15":
        #     record = record._replace(pollingstationpostcode="SA11 2UP")

        # # 'Cwmavon Community Centre, Depot Road, Cwmavon, Port Talbot, SA12 9DF' (id: 147)
        # if record.pollingvenueid == "147":
        #     record = record._replace(pollingstationpostcode="SA12 9BA")

        # # 'Bryn Village Hall, Maesteg Road, Bryn, Port Talbot, SA13 2RY' (id: 23)
        # if record.pollingvenueid == "23":
        #     record = record._replace(pollingstationpostcode="SA13 2RW")

        # # 'Carmel Bethany Presbyterian Church, Off Station Road, (Rear Of Post Office), Port Talbot, SA13 1EJ' (id: 148)
        # if record.pollingvenueid == "148":
        #     record = record._replace(pollingstationpostcode="SA13 1PQ")

        # # 'Sandfields Presbyterian Church, Western Avenue, Port Talbot, SA12 7LZ' (id: 185)
        # if record.pollingvenueid == "185":
        #     record = record._replace(pollingstationpostcode="SA12 7LS")

        # # 'Pelenna Community Centre, Dan Y Coed, Tonmawr, SA12 9UL' (id: 109)
        # if record.pollingvenueid == "109":
        #     record = record._replace(pollingstationpostcode="SA12 9UB")

        # # 'Cilfrew Community Centre, New Road, Cilfrew, SA10 8LL' (id: 64)
        # if record.pollingvenueid == "64":
        #     record = record._replace(pollingstationpostcode="SA10 8AR")

        # # 'Vale of Neath Leisure Centre, Chain Road, Glynneath, Neath, SA11 5HW' (id: 67)
        # if record.pollingvenueid == "67":
        #     record = record._replace(pollingstationpostcode="SA11 5HP")

        # # 'Traherne Court, Stratton Way, Court Herbert, Neath, SA10 7BT' (id: 82)
        # if record.pollingvenueid == "82":
        #     record = record._replace(pollingstationpostcode="SA10 7EE")

        # # 'The Scout Hall, Maes Y Ffynnon Close, Wellfield, Neath, SA11 1HQ' (id: 94)
        # if record.pollingvenueid == "94":
        #     record = record._replace(pollingstationpostcode="SA11 1EZ")

        # # 'Ebenezer Baptist Church, Herbert Road, Melin, Neath, SA11 2DD' (id: 97)
        # if record.pollingvenueid == "97":
        #     record = record._replace(pollingstationpostcode="SA11 2DN")

        # # 'Melincryddan Community Centre, Melincryddan Community Centre, Crythan Road, Neath, SA11 1TB' (id: 98)
        # if record.pollingvenueid == "98":
        #     record = record._replace(pollingstationpostcode="SA11 1SU")

        # # 'The Ganu - Melincourt Community Hall, Lletty Dafydd, Melincourt, SA11 4BW' (id: 116)
        # if record.pollingvenueid == "116":
        #     record = record._replace(pollingstationpostcode="SA11 4DB")

        return super().station_record_to_dict(record)
