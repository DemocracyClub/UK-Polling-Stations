from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAY"
    addresses_name = "2024-07-04/2024-06-11T17:01:00.083806/CAY_combined.csv"
    stations_name = "2024-07-04/2024-06-11T17:01:00.083806/CAY_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "43171669",  # THE LODGE, STABLES COMPOUND, WEST ROAD, PENALLTA INDUSTRIAL ESTATE, PENALLTA, HENGOED
            ]
        ):
            return None
        if record.housepostcode in [
            "NP11 6JE",
            "CF83 8RL",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The council have agreed to the following postcode changes:

        # 'PENYBRYN VILLAGE HALL, TROSNANT CRESCENT, PENYBRYN, HENGOED, CF82 7GF' (id: 25)
        if record.pollingvenueid == "25":
            record = record._replace(pollingstationpostcode="CF82 7FW")

        # 'YSGOL PENALLTAU, CWM CALON ROAD, HENGOED, CF82 7QX' (id: 138)
        if record.pollingvenueid == "138":
            record = record._replace(pollingstationpostcode="CF82 6AP")

        # 'CEFN FFOREST COMMUNITY CENTRE, DERWENDEG AVENUE, CEFN FFOREST, BLACKWOOD, NP12 3JX' (id: 92)
        if record.pollingvenueid == "92":
            record = record._replace(pollingstationpostcode="NP12 3LW")

        # 'PENLLWYN MILLENNIUM CENTRE, PENLLWYN LANE, PONTLLANFRAITH, BLACKWOOD, NP12 2BZ' (id: 150)
        if record.pollingvenueid == "150":
            record = record._replace(pollingstationpostcode="NP12 2EQ")

        # 'RISCA COMMUNITY COMPREHENSIVE SCHOOL, (MUSIC ROOM), PONTYMASON LANE, TRENEWYDD, RISCA, NP11 6GH' (id: 117)
        if record.pollingvenueid == "117":
            record = record._replace(pollingstationpostcode="NP11 6YY")

        # 'GELLIGAER COMMUNITY CENTRE, ANEURIN BEVAN AVENUE, GELLIGAER, HENGOED, CF82 8ET' (id: 23)
        if record.pollingvenueid == "23":
            record = record._replace(pollingstationpostcode="CF82 8ES")

        # 'CASCADE COMMUNITY CENTRE, PENPEDAIRHEOL, HENGOED, CF82 8BX' (id: 26)
        if record.pollingvenueid == "26":
            record = record._replace(pollingstationpostcode="CF82 8BB")

        # 'HENGOED COMMUNITY CENTRE, PARK ROAD, HENGOED, CF82 7LT' (id: 27)
        if record.pollingvenueid == "27":
            record = record._replace(pollingstationpostcode="CF82 7LW")

        # 'CEFN HENGOED COMMUNITY CENTRE, FOREST AVENUE, CEFN HENGOED, HENGOED, CF82 7HY' (id: 34)
        if record.pollingvenueid == "34":
            record = record._replace(pollingstationpostcode="CF82 7HZ")

        # 'NELSON COMMUNITY CENTRE, BRYNCELYN, NELSON, TREHARRIS, CF46 6HN' (id: 37)
        if record.pollingvenueid == "37":
            record = record._replace(pollingstationpostcode="CF46 6HL")

        # 'PENYRHEOL COMMUNITY CENTRE, HEOL ANEURIN, PENYRHEOL, CAERPHILLY, CF83 2PA' (id: 45)
        if record.pollingvenueid == "45":
            record = record._replace(pollingstationpostcode="CF83 2PG")

        # 'HENDREDENNY PARK PRIMARY SCHOOL, GROESWEN DRIVE, HENDREDENNY ESTATE, CAERPHILLY, CF83 2RL' (id: 48)
        if record.pollingvenueid == "48":
            record = record._replace(pollingstationpostcode="CF83 2BL")

        # 'TRETHOMAS CHRISTIAN FELLOWSHIP, STANDARD STREET, TRETHOMAS, CAERPHILLY, CF83 8DH' (id: 60)
        if record.pollingvenueid == "60":
            record = record._replace(pollingstationpostcode="CF83 8DE")

        # 'THE TWYN SCHOOL, (EARLY YEARS UNIT), SOUTHERN STREET, CAERPHILLY, CF83 1LJ' (id: 66)
        if record.pollingvenueid == "66":
            record = record._replace(pollingstationpostcode="CF83 1LH")

        # 'MANMOEL VILLAGE HALL, MANMOEL, BLACKWOOD, NP12 0RH' (id: 86)
        if record.pollingvenueid == "86":
            record = record._replace(pollingstationpostcode="NP12 0RL")

        # 'CWMFELINFACH COMMUNITY CENTRE, STANLEY STREET, CWMFELINFACH, NP11 7HG' (id: 120)
        if record.pollingvenueid == "120":
            record = record._replace(pollingstationpostcode="NP11 7HF")

        # 'ST JOHNS AMBULANCE HALL RISCA, TREDEGAR STREET, RISCA, NP11 6BW' (id: 111)
        if record.pollingvenueid == "111":
            record = record._replace(pollingstationpostcode="NP11 6BY")

        # 'ABERTYSSWG COMMUNITY CENTRE, THE GREEN, ABERTYSSWG, RHYMNEY, NP22 5AN' (id: 5)
        if record.pollingvenueid == "5":
            record = record._replace(pollingstationpostcode="NP22 5AH")

        # 'CARTREF O.A.P. HALL, CARDIFF ROAD, BARGOED, CF81 8NY' (id: 137)
        if record.pollingvenueid == "137":
            record = record._replace(pollingstationpostcode="CF81 8NN")

        # 'GILFACH BARGOED COMMUNITY CENTRE, HEOL PENCARREG, BARGOED, CF81 8QB' (id: 22)
        if record.pollingvenueid == "22":
            record = record._replace(pollingstationpostcode="CF81 8QD")

        # '1ST GILFACH SCOUT HALL, (ST. MARGARETS), REAR OF PARK PLACE, GILFACH, BARGOED, CF81 8LP' (id: 21)
        if record.pollingvenueid == "21":
            record = record._replace(pollingstationpostcode="CF81 8LW")

        return super().station_record_to_dict(record)
