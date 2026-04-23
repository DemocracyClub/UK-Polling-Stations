from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from pollingstations.models import PollingStation
from addressbase.models import Address


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "AGY"
    addresses_name = "2026-05-07/2026-03-05T16:31:00.410075/Democracy Club - Idox_2026-03-05 15-54.csv"
    stations_name = "2026-05-07/2026-03-05T16:31:00.410075/Democracy Club - Idox_2026-03-05 15-54.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "LL65 2ED",
            "LL77 7NW",
            "LL65 2EL",
            "LL65 1BG",
            "LL74 8ST",
            "LL72 8LJ",
        ]:
            return None

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002649098",  # 4 TREMWYLFA, CARMEL, LLANNERCH-Y-MEDD
            "10024357287",  # CHAPEL HOUSE, SOUTH STACK ROAD, HOLYHEAD
            "10013463367",  # HARBOUR HOUSE, TRAETH BYCHAN, MARIANGLAS
            "10013466388",  # OLD GRANARY, PENTRAETH
            "10013853106",  # PANT Y BWLCH, LLANDDONA, BEAUMARIS
            "10013466115",  # RHANDIR, LLANFIGAEL, HOLYHEAD
        ]:
            return None

        return super().address_record_to_dict(record)

    def post_import(self):
        # The a117 data the councils sent had UPRNs for polling stations that weren't in the EMS data
        a11y_uprns = {
            "10-canolfan-gymuned-millbank": 200002645962,
            "11-canolfan-gymuned-kingsland": 200002640997,
            "12-neuadd-y-dref-llangefni": 200002652086,
            "13-neuadd-eglwys-sant-cyngar-llangefni": 10024359640,
            "14-neuadd-y-dref-llangefni": 200002652086,
            "15-canolfan-goffa-gymdeithasol-porthaethwy": 200002639125,
            "16-ysgol-y-borth-porthaethwy": 10013462553,
            "17-canolfan-llanfairynghornwy": 10013851967,
            "18-neuadd-griffith-reade-llanfaethlu": 10013851282,
            "19-neuadd-bentref-llanddeusant": 10013851294,
            "1-canolfan-gymuned-david-hughes-biwmares": 10024356687,
            "20-ysgoldy-capel-m-c-carmel": 10024359645,
            "21-gwesty-holland": 10013851281,
            "22-neuadd-eglwys-sant-mihangel": 10024355360,
            "23-neuadd-eglwys-st-gwenfaen": 10024359646,
            "24-neuadd-gymuned-trearddur": 200002640999,
            "25-y-neuadd-caergeiliog": 10024357560,
            "26-neuadd-bentref-bodedern": 100101029736,
            "27-neuadd-bentref-rhosneigr": 10013852683,
            "28-canolfan-gymuned-llanfaelog": 10024355284,
            "29-canolfan-gymuned-bryngwran": 10013457980,
            "2-neuadd-goffa-amlwch": 200002642873,
            "30-canolfan-gymuned-bodffordd": 10024359641,
            "31-neuadd-goffa-bodwrog": 10013459596,
            "32-canolfan-henoed-gwalchmai": 10013464534,
            "33-neuadd-yr-henoed-llangristiolus": 10013461763,
            "34-neuadd-glannau-ffraw": 10013854101,
            "35-neuadd-bentref-cemaes": 100100962709,
            "36-canolfan-gymuned-llanfechell": 10097361522,
            "37-canolfan-gymuned-carreglefn": 10013466524,
            "38-canolfan-gymuned-rhosybol": 10024357630,
            "39-ysgoldy-capel-mc-parc-llandyfrydog": 10090601853,
            "3-neuadd-goffa-amlwch": 200002642873,
            "40-neuadd-bentref-penysarn": 10013854087,
            "41-neuadd-gymuned-penrhoslligwy": 10024359643,
            "42-neuadd-eglwys-cymuned-moelfre": 10024355307,
            "43-hen-ysgol-marianglas": 10013464161,
            "44-neuadd-bentref-brynteg": 10024355248,
            "45-y-ganolfan-llanbedrgoch": 200002644594,
            "46-llyfrgell-benllech": 200002644232,
            "47-neuadd-gymunedol-a-chyn-filwyr-benllech": 10013459441,
            "48-neuadd-bentref-talwrn": 10024356117,
            "49-ysgoldy-capel-ty-mawr-capel-coch": 10013457838,
            "4-hen-ysgol-porth-amlwch": 200002646021,
            "50-caffi-stesion-llannerchymedd": 10024356674,
            "51-neuadd-goffa-pentraeth": 10024355234,
            "52-neuadd-bentref-llanddona": 10013465450,
            "53-neuadd-bentref-llangoed": 10024356755,
            "54-neuadd-y-plwyf-llandegfan": 200001801343,
            "55-neuadd-goffa-llanfairpwll": 10013852946,
            "56-ysgoldy-capel-ebeneser-llanfairpwll": 10024359635,
            "57-neuadd-bentref-gaerwen": 10013461883,
            "58-yr-efail": 10090602272,
            "59-canolfan-penmynydd": 10013462026,
            "5-neuadd-gymuned-llaingoch": 10024357859,
            "60-canolfan-gymuned-brynsiencyn": 10024356644,
            "61-canolfan-prichard-jones-niwbwrch": 10013462301,
            "62-yr-hen-fecws": 10013461778,
            "63-neuadd-bentref-llangaffo": 10013459107,
            "64-canolfan-hen-ysgol-bodorgan": 10013459250,
            "6-neuadd-y-dref-caergybi": 100100961640,
            "7-neuadd-eglwys-santes-fair": 10097361521,
            "8-canolfan-hyfforddiant-wow": 200002177974,
            "9-neuadd-gymunedol-dewi-sant-caergybi": 10090602655,
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
