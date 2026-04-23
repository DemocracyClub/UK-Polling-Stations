from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from pollingstations.models import PollingStation
from addressbase.models import Address


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "PEM"
    addresses_name = "2026-05-07/2026-02-17T13:17:53.759530/Democracy Club - Idox_2026-02-16 14-31.csv"
    stations_name = "2026-05-07/2026-02-17T13:17:53.759530/Democracy Club - Idox_2026-02-16 14-31.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        record.uprn.strip().lstrip("0")
        if record.uprn in [
            "10013172306",  # HILLFORT PRIORYRATH, HOWARTH CLOSE, MILFORD HAVEN
        ]:
            return None
        if record.postcode in [
            # split
            "SA62 4NJ",
            "SA73 3RA",
            "SA62 3DA",
            "SA62 5RJ",
            "SA62 3PW",
            "SA71 5BP",
            "SA73 1RG",
            "SA73 1BB",
            "SA71 4BP",
            "SA73 1RJ",
            "SA68 0QR",
            "SA72 6BH",
            "SA72 6BE",
            "SA73 3HF",
            "SA73 2EB",
            "SA62 6TD",
            "SA42 0QG",
            "SA73 1BL",
            "SA68 0XN",
            "SA73 1NR",
            "SA67 8RY",
            "SA62 5UD",
            "SA66 7QW",
            "SA62 5DB",
            "SA62 5NL",
            "SA71 4JT",
        ]:
            return None
        return super().address_record_to_dict(record)

    def post_import(self):
        # The a117 data the councils sent had UPRNs for polling stations that weren't in the EMS data
        a11y_uprns = {
            "100-st-davids-city-hall": 200001846098,
            "101-solva-memorial-hall": 100101018641,
            "102-trefgarn-owen-school-room": 10096057318,
            "103-hayscastle-community-centre": 10090688474,
            "104-pen-y-bont-chapel-vestry": 10096056652,
            "105-spittal-church-hall": 10090688463,
            "106-ambleston-memorial-hall": 10013179286,
            "107-llysyfran-yfc-hall": 10091647513,
            "108-maenclochog-community-hall": 10090280586,
            "109-bethel-chapel-vestry": 10096057319,
            "110-llandissilio-village-hall": 10013179311,
            "111-clunderwen-community-hall": 10009896201,
            "112-clarbeston-road-memorial-hall": 10013178412,
            "113-community-hall-crundale": 10013178493,
            "114-camrose-community-centre": 10009872792,
            "115-sutton-baptist-chapel-hall": 10090689368,
            "116-victoria-hall": 10013179173,
            "117-broad-haven-village-hall": 10013179284,
            "118-walwyns-castle-village-hall": 10096056439,
            "119-the-school-room": 10002141280,
            "120-the-institute": 10013179037,
            "121-merlins-bridge-welfare-hall": 10013179059,
            "122-albany-church-hall": 10013177492,
            "123-st-martins-church-hall": 10023955278,
            "124-pembrokeshire-archives": 10090689061,
            "125-haverfordwest-leisure-centre": 10023953244,
            "126-garth-youth-project": 10013170489,
            "127-bethesda-baptist-school-room": 10090689384,
            "128-haverfordwest-cricket-club": 200002959910,
            "129-uzmaston-church-hall": 10090280722,
            "130-freystrop-village-hall": 10013179011,
            "131-hook-sports-and-social-club": 200002960120,
            "132-llangwm-community-centre": 10013179350,
            "133-rosemarket-village-hall": 10013178289,
            "134-burton-jubilee-hall": 10013178880,
            "135-neyland-community-hub-station-1": 10091647002,
            "136-neyland-community-hub-station-2": 10091647002,
            "137-mastlebridge-village-hall": 10013179259,
            "138-st-katharines-parish-hall": 10002141156,
            "139-north-road-baptist-church-school-room-station-1": 10002141158,
            "140-mount-community-centre": 100101023152,
            "141-north-road-baptist-church-school-room-station-2": 10002141158,
            "142-main-hall-christ-church": 100101023681,
            "143-room-at-milford-haven-rugby-club": 10013179014,
            "144-hubberston-and-hakin-youth-and-community-centre": 200002961487,
            "145-church-of-the-holy-sprit": 200002961506,
            "146-herbrandston-community-church-hall": 10096057321,
            "147-st-ishmaels-sports-and-social-club": 10013176569,
            "148-marloes-village-hall": 10013178525,
            "149-dale-coronation-hall-jubilee-suite": 10013170616,
            "150-llanddewi-velfrey-village-hall": 10013178296,
            "151-tavernspite-village-hall": 10013175887,
            "152-narberth-community-library-station-1": 100101019426,
            "153-narberth-community-library-station-2": 100101019426,
            "154-llawhaden-yfc-hall": 10013178784,
            "155-the-rhos-community-hall": 200003264495,
            "156-the-snooty-fox-inn": 10023953220,
            "157-templeton-village-hall": 10090280346,
            "158-amroth-parish-hall": 200002376196,
            "159-regency-hall": 200001854011,
            "160-new-hedges-village-hall": 10009879765,
            "161-tenby-community-learning-centre-station-1": 10013175759,
            "162-tenby-community-learning-centre-station-2": 10013175759,
            "163-kilgetty-begelly-community-centre": 200003248944,
            "164-east-williamston-community-hall": 10013175919,
            "165-the-imperial-dragon-hotel": 200003246980,
            "166-jeffreyston-church-hall": 10096057326,
            "167-carew-memorial-hall": 200002961136,
            "168-st-florence-village-hall": 10013175886,
            "169-penally-village-hall": 10013175865,
            "170-emmanuel-gospel-church": 10096057327,
            "171-lamphey-village-hall": 200002961217,
            "172-cosheston-village-hall": 10013178235,
            "173-pennar-community-hall-station-1": 10090281629,
            "174-pennar-community-hall-station-2": 10090281629,
            "175-st-johns-community-hall-station-1": 10090281293,
            "176-st-johns-community-hall-station-2": 10090281293,
            "177-the-learning-centre": 100101022989,
            "178-pembroke-rugby-club": 200001856336,
            "179-pembroke-town-hall": 100101022349,
            "180-monkton-priory-church-hall": 10096057328,
            "181-pembroke-scout-and-guide-hall": 200003263999,
            "182-castlemartin-village-hall": 10009879774,
            "183-hundleton-sports-pavilion": 10013176087,
            "184-angle-village-hall": 10013178229,
            "77-st-dogmaels-memorial-hall": 10013172900,
            "78-nevern-village-hall": 10023953522,
            "79-moylegrove-old-school-hall": 10013178440,
            "80-yr-hen-ysgol": 10023955247,
            "81-crymych-market-hall": 10013178245,
            "82-cilgerran-village-hall": 10013179300,
            "83-newchapel-reading-room": 10013179301,
            "84-boncath-community-hall": 10013178413,
            "85-canolfan-clydau": 10090280253,
            "86-newport-memorial-hall": 200003249861,
            "87-yr-hen-ysgol": 10009874065,
            "88-town-hall-station-1": 10091644223,
            "89-town-hall-station-2": 10091644223,
            "90-goodwick-scout-hall": 10013177284,
            "91-st-nicholas-village-hall": 10013179207,
            "92-the-gate-inn": 10009895463,
            "93-glandwr-chapel-vestry": 100101062012,
            "94-jabes-chapel-vestry": 10023953803,
            "95-smyrna-chapel-vestry": 10096057317,
            "96-letterston-memorial-hall": 10013179054,
            "97-mathry-community-hall": 10009877321,
            "98-croesgoch-baptist-chapel-vestry": 10090688462,
            "99-trefin-village-hall": 10013178401,
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
