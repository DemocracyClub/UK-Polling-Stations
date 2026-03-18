# settings for councils scraper

EC_COUNCIL_CONTACT_EMAIL = "digitalcommunications@electoralcommission.org.uk"

BOUNDARIES_URL = "https://s3.eu-west-2.amazonaws.com/pollingstations.public.data/ons/boundaries/Local_Authority_Districts_December_2024_Boundaries_UK_BFE.geojson"
COUNCIL_ID_FIELD = "LAD24CD"
EC_COUNCIL_CONTACT_DETAILS_API_URL = (
    "https://electoralcommission.org.uk/api/v1/data/local-authorities.json"
)

OLD_TO_NEW_MAP = {}

NEW_COUNCILS = []

WELSH_COUNCIL_NAMES = {
    "AGY": "Cyngor Sir Ynys Môn",  # Isle of Anglesey County Council
    "BGE": "Cyngor Bwrdeistref Sirol Pen-y-bont ar Ogwr",  # Bridgend County Borough Council
    "BGW": "Cyngor Bwrdeistref Sirol Blaenau Gwent",  # Blaenau Gwent County Borough Council
    "CAY": "Cyngor Bwrdeistref Sirol Caerffili",  # Caerphilly County Borough Council
    "CGN": "Cyngor Sir Ceredigion",  # Ceredigion County Council
    "CMN": "Cyngor Sir Gaerfyrddin",  # Carmarthenshire County Council
    "CRF": "Cyngor Caerdydd",  # Cardiff Council
    "CWY": "Cyngor Bwrdeistref Sirol Conwy",  # Conwy County Borough Council
    "DEN": "Cyngor Sir Ddinbych",  # Denbighshire County Council
    "FLN": "Cyngor Sir y Fflint",  # Flintshire County Council
    "GWN": "Cyngor Sir Gwynedd",  # Gwynedd Council
    "MON": "Cyngor Sir Fynwy",  # Monmouthshire County Council
    "MTY": "Cyngor Bwrdeistref Sirol Merthyr Tudful",  # Merthyr Tydfil County Borough Council
    "NTL": "Cyngor Bwrdeistref Sirol Castell-nedd Port Talbot",  # Neath Port Talbot County Borough Council
    "NWP": "Cyngor Dinas Casnewydd",  # Newport City Council
    "PEM": "Cyngor Sir Penfro",  # Pembrokeshire County Council
    "POW": "Cyngor Sir Powys",  # Powys County Council
    "RCT": "Cyngor Bwrdeistref Sirol Rhondda Cynon Taf",  # Rhondda Cynon Taf County Borough Council
    "SWA": "Cyngor Sir a Dinas Abertawe",  # City and County of Swansea
    "TOF": "Cyngor Bwrdeistref Sirol Torfaen",  # Torfaen County Borough Council
    "VGL": "Cyngor Bwrdeistref Sirol Bro Morgannwg",  # The Vale of Glamorgan County Borough Council
    "WRX": "Cyngor Bwrdeistref Sirol Wrecsam",  # Wrexham County Borough Council
}

NIR_IDS = [
    "ABC",
    "AND",
    "ANN",
    "BFS",
    "CCG",
    "DRS",
    "FMO",
    "LBC",
    "MEA",
    "MUL",
    "NMD",
]

# Based on https://www.legislation.gov.uk/ssi/2025/287/schedule/2/made
SP_CONSTITUENCY_26_ID_TO_CONTACT_DETAILS = {
    "sp.c.aberdeen-deeside-and-north-kincardine.2026-05-07": {
        "name": "Aberdeen City Council",
        "electoral_services_email": "elections@aberdeencity.gov.uk",
        "electoral_services_website": "https://www.aberdeencity.gov.uk",
        "electoral_services_postcode": "AB10 1AB",
        "electoral_services_address": "Marischal College\r\nAberdeen\r\nAB10 1AB",
        "electoral_services_phone_numbers": ["01224 522115"],
    },
    "sp.c.angus-north-and-mearns.2026-05-07": {
        "name": "Angus Council",
        "electoral_services_email": "elections@angus.gov.uk",
        "electoral_services_website": "http://www.angus.gov.uk",
        "electoral_services_postcode": "DD8 1AN",
        "electoral_services_address": "Angus House\r\nOrchardbank Business Park\r\nOrchardbank\r\nForfar\r\nAngus\r\nDD8 1AN",
        "electoral_services_phone_numbers": ["01307 491 781"],
    },
    "sp.c.banffshire-and-buchan-coast.2026-05-07": {
        "name": "Aberdeenshire Council",
        "electoral_services_email": "elections@aberdeenshire.gov.uk",
        "electoral_services_website": "http://www.aberdeenshire.gov.uk",
        "electoral_services_postcode": "AB16 5GB",
        "electoral_services_address": "Woodhill House\r\nWestburn Road\r\nAberdeen\r\nAB16 5GB",
        "electoral_services_phone_numbers": ["01467 539 311"],
    },
    "sp.c.carrick-cumnock-and-doon-valley.2026-05-07": {
        "name": "East Ayrshire Council",
        "electoral_services_email": "electionoffice@east-ayrshire.gov.uk",
        "electoral_services_website": "https://www.east-ayrshire.gov.uk",
        "electoral_services_postcode": "KA3 7BU",
        "electoral_services_address": "London Road\r\nKilmarnock\r\nEast Ayrshire\r\nKA3 7BU",
        "electoral_services_phone_numbers": ["01563 576 555"],
    },
    "sp.c.clackmannanshire-and-dunblane.2026-05-07": {
        "name": "Clackmannanshire Council",
        "electoral_services_email": "elections@clacks.gov.uk",
        "electoral_services_website": "https://www.clacks.gov.uk",
        "electoral_services_postcode": "FK10 1EB",
        "electoral_services_address": "Kilncraigs\r\nGreenside Street\r\nAlloa\r\nFK10 1EB",
        "electoral_services_phone_numbers": ["01259 452266"],
    },
    "sp.c.clydebank-and-milngavie.2026-05-07": {
        "name": "West Dunbartonshire Council",
        "electoral_services_email": "elections@west-dunbarton.gov.uk",
        "electoral_services_website": "https://www.west-dunbarton.gov.uk",
        "electoral_services_postcode": "",
        "electoral_services_address": "",
        "electoral_services_phone_numbers": ["01389 737204"],
    },
    "sp.c.cunninghame-south.2026-05-07": {
        "name": "North Ayrshire Council",
        "electoral_services_email": "elections@north-ayrshire.gov.uk",
        "electoral_services_website": "https://www.north-ayrshire.gov.uk",
        "electoral_services_postcode": "KA12 8EE",
        "electoral_services_address": "Cunninghame House\r\nIrvine\r\nScotland\r\nKA12 8EE",
        "electoral_services_phone_numbers": ["01294 324 710"],
    },
    "sp.c.dumbarton.2026-05-07": {
        "name": "West Dunbartonshire Council",
        "electoral_services_email": "elections@west-dunbarton.gov.uk",
        "electoral_services_website": "https://www.west-dunbarton.gov.uk",
        "electoral_services_postcode": "",
        "electoral_services_address": "",
        "electoral_services_phone_numbers": ["01389 737204"],
    },
    "sp.c.edinburgh-eastern-musselburgh-and-tranent.2026-05-07": {
        "name": "East Lothian Council",
        "electoral_services_email": "elections@eastlothian.gov.uk",
        "electoral_services_website": "https://www.eastlothian.gov.uk/",
        "electoral_services_postcode": "EH41 3HA",
        "electoral_services_address": "John Muir House\r\nBrewery Park\r\nHaddington\r\nEast Lothian\r\nEH41 3HA",
        "electoral_services_phone_numbers": ["01620 827 827"],
    },
    "sp.c.falkirk-east-and-linlithgow.2026-05-07": {
        "name": "Falkirk Council",
        "electoral_services_email": "elections@falkirk.gov.uk",
        "electoral_services_website": "https://www.falkirk.gov.uk",
        "electoral_services_postcode": "FK5 4RU",
        "electoral_services_address": "4 Central Boulevard\r\nCentral Park\r\nLarbert\r\nFK5 4RU",
        "electoral_services_phone_numbers": ["01324 506152"],
    },
    "sp.c.midlothian-south-tweeddale-and-lauderdale.2026-05-07": {
        "name": "Scottish Borders Council",
        "electoral_services_email": "Electoral.Registration@scotborders.gov.uk",
        "electoral_services_website": "https://www.saa.gov.uk/scottishborders/electoral-registration/",
        "electoral_services_postcode": "TD6 6BQ",
        "electoral_services_address": "Electoral Registration Officer \r\nPO Box 13639 \r\nCouncil Headquarters \r\nNewtown St Boswells \r\nMELROSE",
        "electoral_services_phone_numbers": ["01835 825100"],
    },
    "sp.c.renfrewshire-north-and-cardonald.2026-05-07": {
        "name": "Renfrewshire Council",
        "electoral_services_email": "election-office@renfrewshire.gov.uk",
        "electoral_services_website": "https://www.renfrewshire.gov.uk/",
        "electoral_services_postcode": "PA3 9UW",
        "electoral_services_address": "Renfrewshire House\r\nCotton St\r\nPaisley\r\nPA3 9UW",
        "electoral_services_phone_numbers": ["0141 618 2300"],
    },
    "sp.c.renfrewshire-west-and-levern-valley.2026-05-07": {
        "name": "Renfrewshire Council",
        "electoral_services_email": "election-office@renfrewshire.gov.uk",
        "electoral_services_website": "https://www.renfrewshire.gov.uk/",
        "electoral_services_postcode": "PA3 9UW",
        "electoral_services_address": "Renfrewshire House\r\nCotton St\r\nPaisley\r\nPA3 9UW",
        "electoral_services_phone_numbers": ["0141 618 2300"],
    },
    "sp.c.uddingston-and-bellshill.2026-05-07": {
        "name": "North Lanarkshire Council",
        "electoral_services_email": "electionoffice@northlan.gov.uk",
        "electoral_services_website": "https://www.northlanarkshire.gov.uk/",
        "electoral_services_postcode": "",
        "electoral_services_address": "",
        "electoral_services_phone_numbers": ["01698 302 119 / 302331"],
    },
}
