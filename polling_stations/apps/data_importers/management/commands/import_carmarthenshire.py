from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CMN"
    addresses_name = "2021-03-15T10:00:39.477972/Camarthenshire polling_station_export-2021-03-12.csv"
    stations_name = "2021-03-15T10:00:39.477972/Camarthenshire polling_station_export-2021-03-12.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10004879008",  # GARREG, LLANSAWEL, LLANDEILO
            "10004875969",  # GAREG, CAIO, LLANWRDA
            "10009546779",  # PENGOILAN, BETHLEHEM, LLANDEILO
            "10004876729",  # CEFNCETHIN FARMHOUSE, FFAIRFACH, LLANDEILO
            "10024326581",  # PEN Y COED, LLANDYFAN, AMMANFORD
            "10090705407",  # CASTELL IORWG, TALOG, CARMARTHEN
            "10004875097",  # DANYDDERWEN, GELLYWEN, CARMARTHEN
            "10009163588",  # PANTYRHEDYN, GELLYWEN, CARMARTHEN
            "10009162943",  # BRYNHYFRYD, CWMFELIN BOETH, WHITLAND
            "10004868779",  # HAFAN, CWMFELIN BOETH, WHITLAND
            "10009162599",  # PENCLIPPIN CROSSING COTTAGE, LOGIN, WHITLAND
            "10004869095",  # WEST MARSH FARM, LAUGHARNE, CARMARTHEN
            "10004848463",  # MERRY VALE, HALFPENNY FURZE, LAUGHARNE, CARMARTHEN
            "10009163428",  # DANYCOED, LLANDDOWROR, ST. CLEARS, CARMARTHEN
            "10090702596",  # FLAT, CLARE HOUSE, PENTRE ROAD, ST. CLEARS, CARMARTHEN
            "10004881241",  # ROCK COTTAGE, GWSCWM ROAD, PEMBREY, BURRY PORT
            "10004852250",  # 79 GWSCWM ROAD, PEMBREY, BURRY PORT
            "10004852249",  # 77 GWSCWM ROAD, PEMBREY, BURRY PORT
            "10004880395",  # QUARRY BACH FARM, PONTYBEREM, LLANELLI
            "10004880394",  # BLAENLLIEDI FARM, PONTYBEREM, LLANELLI
            "10009543538",  # GYSCOD YR ONNEN, CROSS HANDS, LLANELLI
            "10004881656",  # HONEY WELL, CROSS HANDS, LLANELLI
            "10004881661",  # RHOS FACH FARM, CROSS HANDS, LLANELLI
            "100100170154",  # 57 GELLI ROAD, LLANELLI
            "100100170152",  # 55 GELLI ROAD, LLANELLI
            "100101000942",  # 29 FELINFOEL ROAD, LLANELLI
            "10009170338",  # FLAT 2, 3 STATION ROAD, LLANELLI
            "200001731144",  # TY LLWYD FACH, THORNHILL ROAD, CWMGWILI, LLANELLI
            "100100158334",  # TYNEWYDD, THORNHILL ROAD, CWMGWILI, LLANELLI
            "200001871204",  # OAKWOOD HOUSE, GLYNHIR ROAD, LLANDYBIE, AMMANFORD
            "100101004543",  # GARDEN COTTAGE, GLYNHIR ROAD, LLANDYBIE, AMMANFORD
            "10004879154",  # BRONHAUL, TALLEY, LLANDEILO
            "10004872417",  # PEN-GELLY-ISAF, LLANGAIN, CARMARTHEN
            "10004879184",  # FRON HAUL, TALLEY, LLANDEILO
            "10024323307",  # GLENABBEY, ALLTWALIS ROAD, ALLTWALIS, CARMARTHEN
            "10009162987",  # PENYGRAIG, WHITLAND
        ]:
            return None

        if record.housepostcode in [
            "SA33 6HB",
            "SA31 3JJ",
            "SA33 5DL",
            "SA34 0XA",
            "SA34 0HX",
            "SA33 5QQ",
            "SA33 5DH",
            "SA32 7AS",
            "SA14 8BZ",
            "SA32 8BX",
            "SA17 4NF",
            "SA39 9EJ",
            "SA44 5YB",
            "SA15 1HP",
            "SA32 7QJ",
            "SA17 5US",
            "SA18 2SU",
            "SA19 8TA",
            "SA19 8BR",
            "SA19 7SG",
            "SA20 0EY",
            "SA19 7DL",
            "SA18 3TB",
            "SA18 3NB",
            "SA19 7YE",
            "SA19 9AS",
            "SA16 0PP",
            "SA16 0LE",
            "SA16 0PB",
            "SA14 9AW",
            "SA14 8JA",
            "SA14 8AY",
            "SA14 8TP",
            "SA15 5LP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # VILLAGE HALL LLANGATHEN NEUADD Y PENTREF LLANGATHEN SA32  8Q
        if (
            record.pollingstationnumber == "71"
            and record.pollingstationpostcode == "SA32  8Q"
        ):
            record = record._replace(pollingstationpostcode="")

        # CAPEL IWAN COMMUNITY CENTRE CANOLFAN GYMDEITHASOL CAPEL IWAN . SA38 9SL
        if (
            record.pollingstationnumber == "4"
            and record.pollingstationpostcode == "SA38 9SL"
        ):
            record = record._replace(pollingstationpostcode="")

        # COMMUNITY HALL PONTHENRI Y NEUADD GYMUNEDOL PONTHENRI SA15 5TY
        if (
            record.pollingstationnumber == "107"
            and record.pollingstationpostcode == "SA15 5TY"
        ):
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
