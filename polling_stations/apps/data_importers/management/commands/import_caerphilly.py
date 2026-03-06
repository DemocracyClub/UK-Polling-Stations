from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CAY"
    addresses_name = "2026-05-07/2026-03-06T15:00:55.342358/CAY_combined.csv"
    stations_name = "2026-05-07/2026-03-06T15:00:55.342358/CAY_combined.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "43008306",  # TRE EVANS HOUSE, TRE EVANS, RHYMNEY, TREDEGAR
        ]:
            return None

        if record.postcode in [
            # split
            "NP12 1JN",
            "NP11 6JE",
            "CF83 8RL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The council have agreed to the following postcode changes:

        # PENYBRYN VILLAGE HALL, TROSNANT CRESCENT, PENYBRYN, HENGOED, CF82 7GF
        if record.pollingvenueid == "25":
            record = record._replace(pollingstationpostcode="CF82 7FW")

        # CEFN FFOREST COMMUNITY CENTRE, DERWENDEG AVENUE, CEFN FFOREST, BLACKWOOD, NP12 3JX
        if record.pollingvenueid == "92":
            record = record._replace(pollingstationpostcode="NP12 3LW")

        # PENLLWYN MILLENNIUM CENTRE, PENLLWYN LANE, PONTLLANFRAITH, BLACKWOOD, NP12 2BZ
        if record.pollingvenueid == "150":
            record = record._replace(pollingstationpostcode="NP12 2EQ")

        # RISCA COMMUNITY COMPREHENSIVE SCHOOL, (MUSIC ROOM), PONTYMASON LANE, TRENEWYDD, RISCA, NP11 6GH
        if record.pollingvenueid == "117":
            record = record._replace(pollingstationpostcode="NP11 6YY")

        # GELLIGAER COMMUNITY CENTRE, ANEURIN BEVAN AVENUE, GELLIGAER, HENGOED, CF82 8ET
        if record.pollingvenueid == "23":
            record = record._replace(pollingstationpostcode="CF82 8ES")

        # CASCADE COMMUNITY CENTRE, PENPEDAIRHEOL, HENGOED, CF82 8BX
        if record.pollingvenueid == "26":
            record = record._replace(pollingstationpostcode="CF82 8BB")

        # HENGOED COMMUNITY CENTRE, PARK ROAD, HENGOED, CF82 7LT
        if record.pollingvenueid == "27":
            record = record._replace(pollingstationpostcode="CF82 7LW")

        # MANMOEL VILLAGE HALL, MANMOEL, BLACKWOOD, NP12 0RH
        if record.pollingvenueid == "86":
            record = record._replace(pollingstationpostcode="NP12 0RL")

        # CWMFELINFACH COMMUNITY CENTRE, STANLEY STREET, CWMFELINFACH, NP11 7HG
        if record.pollingvenueid == "120":
            record = record._replace(pollingstationpostcode="NP11 7HF")

        # SGILIAU CBC FORMER ST JOHNS AMBULANCE HALL RISCA, TREDEGAR STREET, RISCA, NP11 6BW
        if record.pollingvenueid == "111":
            record = record._replace(pollingstationpostcode="NP11 6BY")

        # ABERTYSSWG COMMUNITY CENTRE, THE GREEN, ABERTYSSWG, RHYMNEY, NP22 5AN
        if record.pollingvenueid == "5":
            record = record._replace(pollingstationpostcode="NP22 5AH")

        # 1ST GILFACH SCOUT HALL, (ST. MARGARETS), REAR OF PARK PLACE, GILFACH, BARGOED, CF81 8LP
        if record.pollingvenueid == "21":
            record = record._replace(pollingstationpostcode="CF81 8LW")

        return super().station_record_to_dict(record)
