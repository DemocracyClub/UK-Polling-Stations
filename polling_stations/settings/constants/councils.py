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
# Maps SP constituency ballot IDs to the council_id of the responsible
# council, so contact details can be looked up from the database.
SP_CONSTITUENCY_26_BALLOT_TO_COUNCIL = {
    "sp.c.aberdeen-deeside-and-north-kincardine.2026-05-07": "ABE",  # Aberdeen City Council
    "sp.c.angus-north-and-mearns.2026-05-07": "ANS",  # Angus Council
    "sp.c.banffshire-and-buchan-coast.2026-05-07": "ABD",  # Aberdeenshire Council
    "sp.c.carrick-cumnock-and-doon-valley.2026-05-07": "EAY",  # East Ayrshire Council
    "sp.c.clackmannanshire-and-dunblane.2026-05-07": "CLK",  # Clackmannanshire Council
    "sp.c.clydebank-and-milngavie.2026-05-07": "WDU",  # West Dunbartonshire Council
    "sp.c.cunninghame-south.2026-05-07": "NAY",  # North Ayrshire Council
    "sp.c.dumbarton.2026-05-07": "WDU",  # West Dunbartonshire Council
    "sp.c.edinburgh-eastern-musselburgh-and-tranent.2026-05-07": "ELN",  # East Lothian Council
    "sp.c.falkirk-east-and-linlithgow.2026-05-07": "FAL",  # Falkirk Council
    "sp.c.midlothian-south-tweeddale-and-lauderdale.2026-05-07": "SCB",  # Scottish Borders Council
    "sp.c.renfrewshire-north-and-cardonald.2026-05-07": "RFW",  # Renfrewshire Council
    "sp.c.renfrewshire-west-and-levern-valley.2026-05-07": "RFW",  # Renfrewshire Council
    "sp.c.uddingston-and-bellshill.2026-05-07": "NLK",  # North Lanarkshire Council
}
