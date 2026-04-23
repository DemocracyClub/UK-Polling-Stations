from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from pollingstations.models import PollingStation
from addressbase.models import Address


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
        # UPRN change for station:
        # THE NOOK CAFE FORMER PUDDLERS ARMS PLANTATION TERRACE RHYMNEY TREDEGAR NP22 5PX
        if self.get_station_hash(record) == "4-the-nook-cafe-former-puddlers-arms":
            record = record._replace(pollingvenueuprn="43180671")

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

        # GELLIGAER BOWLS CLUB, THE RECREATION GROUND, GLYNGAER, GELLIGAER, CF82 8FJ
        if record.pollingvenueid == "164":
            record = record._replace(pollingstationpostcode="CF82 8BU")

        # PWLLYPANT VILLAGE HALL, WILKINS TERRACE, LLANBRADACH, CAERPHILLY, CF83 2NH
        if record.pollingvenueid == "41":
            record = record._replace(pollingstationpostcode="CF83 3SA")

        # ST JOHNS AMBULANCE HALL PONTLLANFRAITH, ISLWYN PARK, LLANARTH ROAD, SPRINGFIELD, PONTLLANFRAITH, NP12 2LN
        if record.pollingvenueid == "102":
            record = record._replace(pollingstationpostcode="NP12 2LG")
        return super().station_record_to_dict(record)

    def post_import(self):
        # The a117 data the councils sent had UPRNs for polling stations that weren't in the EMS data
        a11y_uprns = {
            "10-flying-start-unit-pantside-primary-school": 43169906,
            "13-pentwynmawr-community-centre": 43087905,
            "13-phillipstown-community-centre": 43091642,
            "15-abercarn-rugby-club": 43091470,
            "15-george-inn": 43084907,
            "17-new-life-christian-church": 43066785,
            "18-cwmcarn-army-cadet-force-centre": 43164528,
            "19-cwmcarn-zion-baptist-church": 4306980,
            "1-st-aidans-church": 43168829,
            "20-st-gwladys-church-hall": 43164744,
            "25-libanus-christian-community-centre": 43168918,
            "26-plas-mawr-community-centre": 43171605,
            "27-blackwood-bowls-club": 43076173,
            "29-st-thomas-church-hall": 43175083,
            "31-oakdale-sports-pavilion": 43091472,
            "32-woodfieldside-oap-hall": 43175084,
            "33-crosskeys-methodist-church-hall": 43175077,
            "34-cefn-hengoed-youth-centre": 43090886,
            "34-trinity-congregational-church-hall": 43084934,
            # "35-crosskeys-rugby-club": 43065439,
            "36-lewis-street-methodist-church": 43019844,
            "37-bethania-chapel": 43167573,
            "38-lewis-street-methodist-church": 43019844,
            "39-st-margarets-church-hall": 43169818,
            "40-calfaria-baptist-church": 43007856,
            "40-the-pavilion-pontymister": 43165821,
            # "43-channel-view-community-centre": 43091435,
            "44-ebenezer-church-hall": 43169821,
            "4-crumlin-rugby-club": 43068461,
            "57-groeswen-congregational-chapel": 43085819,
            "6-st-tyfaelogs-church-hall": 43169662,
            "71-2nd-caerphilly-scout-hall": 43091413,
            "73-2nd-caerphilly-scout-hall": 43091413,
            "7-deri-community-centre": 43090834,
            "80-graig-y-rhacca-community-centre": 43167887,
            "83-lansbury-park-housing-office": 43034008,
            "87-fleur-de-lis-community-centre": 43164692,
            "88-st-davids-church-hall": 1005333270,
            "90-fresh-hair": 43043984,
            "96-st-augustines-church-hall": 43052819,
            # "9-flying-start-unit-pantside-primary-school": 43169907,
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
