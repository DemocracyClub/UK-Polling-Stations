from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from pollingstations.models import PollingStation
from addressbase.models import Address


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
        # Council says to ignore the following postcode mismatch warnings:
        # Cwmavon Community Centre, Depot Road, Cwmavon, Port Talbot, SA12 9DF
        # Vale of Neath Leisure Centre, Chain Road, Glynneath, Neath, SA11 5HW
        # The Scout Hall, Maes Y Ffynnon Close, Wellfield, Neath, SA11 1HQ

        # postcode correction for: Godrergraig Workingmens Club, Glanyrafon Road, Ystalyfera, SA9 2HA
        if self.get_station_hash(record) == "826-godrergraig-workingmens-club":
            record = record._replace(pollingstationpostcode="SA9 2DE")

        # 'Aberavon Community Resource Centre (NSA), Michna Street, Port Talbot, SA12 6UH' (id: 3)
        if record.pollingvenueid == "3":
            record = record._replace(pollingstationpostcode="SA12 6LR")

        # 'Baglan Community Centre, Hawthorn Avenue, Baglan, SA12 8PG' (id: 11)
        if record.pollingvenueid == "11":
            record = record._replace(pollingstationpostcode="SA12 8PH")

        # 'Hengwrt Community Sports Centre, Llansawel Crescent, Briton Ferry, Neath, SA11 2UW' (id: 15)
        if record.pollingvenueid == "15":
            record = record._replace(pollingstationpostcode="SA11 2UP")

        # 'Bryn Village Hall, Maesteg Road, Bryn, Port Talbot, SA13 2RY' (id: 23)
        if record.pollingvenueid == "23":
            record = record._replace(pollingstationpostcode="SA13 2RW")

        # 'Carmel Bethany Presbyterian Church, Off Station Road, (Rear Of Post Office), Port Talbot, SA13 1EJ' (id: 148)
        if record.pollingvenueid == "148":
            record = record._replace(pollingstationpostcode="SA13 1PQ")

        # 'Sandfields Presbyterian Church, Western Avenue, Port Talbot, SA12 7LZ' (id: 185)
        if record.pollingvenueid == "185":
            record = record._replace(pollingstationpostcode="SA12 7LS")

        # 'Pelenna Community Centre, Dan Y Coed, Tonmawr, SA12 9UL' (id: 109)
        if record.pollingvenueid == "109":
            record = record._replace(pollingstationpostcode="SA12 9UB")

        # 'Cilfrew Community Centre, New Road, Cilfrew, SA10 8LL' (id: 64)
        if record.pollingvenueid == "64":
            record = record._replace(pollingstationpostcode="SA10 8AR")

        # 'Traherne Court, Stratton Way, Court Herbert, Neath, SA10 7BT' (id: 82)
        if record.pollingvenueid == "82":
            record = record._replace(pollingstationpostcode="SA10 7EE")

        # 'Ebenezer Baptist Church, Herbert Road, Melin, Neath, SA11 2DD' (id: 97)
        if record.pollingvenueid == "97":
            record = record._replace(pollingstationpostcode="SA11 2DN")

        # 'Melincryddan Community Centre, Melincryddan Community Centre, Crythan Road, Neath, SA11 1TB' (id: 98)
        if record.pollingvenueid == "98":
            record = record._replace(pollingstationpostcode="SA11 1SU")

        # 'The Ganu - Melincourt Community Hall, Lletty Dafydd, Melincourt, SA11 4BW' (id: 116)
        if record.pollingvenueid == "116":
            record = record._replace(pollingstationpostcode="SA11 4DB")

        return super().station_record_to_dict(record)

    def post_import(self):
        # The a117 data the councils sent had UPRNs for polling stations that weren't in the EMS data
        a11y_uprns = {
            "14-tabernacle-chapel": 10009185692,
            "16-rock-chapel-vestry": 10023948786,
            "1-st-marys-centre": 10009188044,
            "20-afan-christian-fellowship": 10023947135,
            "26-round-chapel-vestry-beulah": 10009187713,
            "27-bertha-community-centre": 200002955824,
            "29-wesley-church-schoolroom": 10009186752,
            "34-aberavon-green-stars-rfc": 200002955636,
            "3-bethlehem-evangelical-church": 10009186134,
            "5-ebenezer-chapel-vestry": 10009186068,
            "802-aberdulais-community-centre": 10009186156,
            "803-st-johns-church-hall": 10023949072,
            "810-cadoxton-community-centre": 10009186157,
            "820-the-community-hall": 10009185181,
            "823-dyffryn-clydach-memorial-hall": 10009187888,
            "825-glynneath-town-hall": 100101040063,
            "827-community-hall": 10023949024,
            "835-neath-civic-centre": 10009179669,
            "837-clive-roberts-hall-cimla-scout-hall": 10009186960,
            "838-st-josephs-rc-church-hall": 10009186073,
            "841-alltycham-rhydyfro-community-hall": 10009185155,
            "843-clyne-community-centre": 100101040321,
            "845-sardis-chapel-vestry": 10009186142,
            "846-noddfa-newydd-baptist-church": 10014160520,
            "847-the-community-centre": 100101040731,
            "848-trebanos-community-hall": 200002961591,
            "852-mission-hall": 10009185742,
            "855-jersey-marine-methodist-church": 10009185744,
            "856-bay-studios": 10014165056,
        }

        for station_id, uprn in a11y_uprns.items():
            try:
                ps = PollingStation.objects.get(internal_council_id=station_id)
                if not ps.location:
                    address = Address.objects.get(uprn=uprn)
                    ps.location = address.location
                    ps.save()
            except (PollingStation.DoesNotExist, Address.DoesNotExist):
                continue
