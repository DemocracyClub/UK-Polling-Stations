from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAY"
    addresses_name = (
        "2025-10-23/2025-09-22T17:23:19.506480/SupportSql_20250922_171609.csv"
    )
    stations_name = (
        "2025-10-23/2025-09-22T17:23:19.506480/SupportSql_20250922_171609.csv"
    )
    elections = ["2025-10-23"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CF83 8RL",  # split
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The council have agreed to the following postcode changes:

        # 'PENYBRYN VILLAGE HALL, TROSNANT CRESCENT, PENYBRYN, HENGOED, CF82 7GF'
        if record.pollingvenueid == "25":
            record = record._replace(pollingstationpostcode="CF82 7FW")

        # 'YSGOL PENALLTAU, CWM CALON ROAD, HENGOED, CF82 7QX'
        if record.pollingvenueid == "138":
            record = record._replace(pollingstationpostcode="CF82 6AP")

        # # 'CEFN FFOREST COMMUNITY CENTRE, DERWENDEG AVENUE, CEFN FFOREST, BLACKWOOD, NP12 3JX'
        # if record.pollingvenueid == "92":
        #     record = record._replace(pollingstationpostcode="NP12 3LW")

        # # 'PENLLWYN MILLENNIUM CENTRE, PENLLWYN LANE, PONTLLANFRAITH, BLACKWOOD, NP12 2BZ'
        # if record.pollingvenueid == "150":
        #     record = record._replace(pollingstationpostcode="NP12 2EQ")

        # # 'RISCA COMMUNITY COMPREHENSIVE SCHOOL, (MUSIC ROOM), PONTYMASON LANE, TRENEWYDD, RISCA, NP11 6GH'
        # if record.pollingvenueid == "117":
        #     record = record._replace(pollingstationpostcode="NP11 6YY")

        # 'GELLIGAER COMMUNITY CENTRE, ANEURIN BEVAN AVENUE, GELLIGAER, HENGOED, CF82 8ET'
        if record.pollingvenueid == "23":
            record = record._replace(pollingstationpostcode="CF82 8ES")

        # 'CASCADE COMMUNITY CENTRE, PENPEDAIRHEOL, HENGOED, CF82 8BX'
        if record.pollingvenueid == "26":
            record = record._replace(pollingstationpostcode="CF82 8BB")

        # 'HENGOED COMMUNITY CENTRE, PARK ROAD, HENGOED, CF82 7LT'
        if record.pollingvenueid == "27":
            record = record._replace(pollingstationpostcode="CF82 7LW")

        # 'CEFN HENGOED COMMUNITY CENTRE, FOREST AVENUE, CEFN HENGOED, HENGOED, CF82 7HY'
        if record.pollingvenueid == "34":
            record = record._replace(pollingstationpostcode="CF82 7HZ")

        # 'NELSON COMMUNITY CENTRE, BRYNCELYN, NELSON, TREHARRIS, CF46 6HN'
        if record.pollingvenueid == "37":
            record = record._replace(pollingstationpostcode="CF46 6HL")

        # 'PENYRHEOL COMMUNITY CENTRE, HEOL ANEURIN, PENYRHEOL, CAERPHILLY, CF83 2PA'
        if record.pollingvenueid == "45":
            record = record._replace(pollingstationpostcode="CF83 2PG")

        # 'HENDREDENNY PARK PRIMARY SCHOOL, GROESWEN DRIVE, HENDREDENNY ESTATE, CAERPHILLY, CF83 2RL'
        if record.pollingvenueid == "48":
            record = record._replace(pollingstationpostcode="CF83 2BL")

        # # 'TRETHOMAS CHRISTIAN FELLOWSHIP, STANDARD STREET, TRETHOMAS, CAERPHILLY, CF83 8DH'
        # if record.pollingvenueid == "60":
        #     record = record._replace(pollingstationpostcode="CF83 8DE")

        # 'THE TWYN SCHOOL, (EARLY YEARS UNIT), SOUTHERN STREET, CAERPHILLY, CF83 1LJ'
        if record.pollingvenueid == "66":
            record = record._replace(pollingstationpostcode="CF83 1LH")

        # # 'MANMOEL VILLAGE HALL, MANMOEL, BLACKWOOD, NP12 0RH'
        # if record.pollingvenueid == "86":
        #     record = record._replace(pollingstationpostcode="NP12 0RL")

        # # 'CWMFELINFACH COMMUNITY CENTRE, STANLEY STREET, CWMFELINFACH, NP11 7HG'
        # if record.pollingvenueid == "120":
        #     record = record._replace(pollingstationpostcode="NP11 7HF")

        # # 'ST JOHNS AMBULANCE HALL RISCA, TREDEGAR STREET, RISCA, NP11 6BW'
        # if record.pollingvenueid == "111":
        #     record = record._replace(pollingstationpostcode="NP11 6BY")

        # # 'ABERTYSSWG COMMUNITY CENTRE, THE GREEN, ABERTYSSWG, RHYMNEY, NP22 5AN'
        # if record.pollingvenueid == "5":
        #     record = record._replace(pollingstationpostcode="NP22 5AH")

        # 'CARTREF O.A.P. HALL, CARDIFF ROAD, BARGOED, CF81 8NY'
        if record.pollingvenueid == "137":
            record = record._replace(pollingstationpostcode="CF81 8NN")

        # 'GILFACH BARGOED COMMUNITY CENTRE, HEOL PENCARREG, BARGOED, CF81 8QB'
        if record.pollingvenueid == "22":
            record = record._replace(pollingstationpostcode="CF81 8QD")

        # '1ST GILFACH SCOUT HALL, (ST. MARGARETS), REAR OF PARK PLACE, GILFACH, BARGOED, CF81 8LP'
        if record.pollingvenueid == "21":
            record = record._replace(pollingstationpostcode="CF81 8LW")

        # Waiting on council confirmation for the following:

        # # 'TRECENYDD COMMUNITY CENTRE, SECOND AVENUE, TRECENYDD, CAERPHILLY, CF83 2SN' (id: 135)
        # if record.pollingvenueid == "135":
        #     record = record._replace(pollingstationpostcode="CF83 2SG")

        # # 'TONYFELIN WELSH BAPTIST CHAPEL, BEDWAS ROAD, CAERPHILLY, CF83 1PD' (id: 49)
        # if record.pollingvenueid == "49":
        #     record = record._replace(pollingstationpostcode="CF83 1PA")

        # 'TRETHOMAS LIFE CENTRE, HEOL YR YSGOL, TRETHOMAS, CAERPHILLY, CF83 8FL' (id: 60)
        if record.pollingvenueid == "60":
            # record = record._replace(pollingstationpostcode="CF83 8DE")
            record = record._replace(pollingvenueuprn="43091261")

        # 'PORTA CABIN in LAY-BY, MAFON ROAD (Close to Railway Inn)' (id: 36)
        if record.pollingvenueid == "36":
            record = record._replace(pollingvenueuprn="43088144")

        return super().station_record_to_dict(record)
