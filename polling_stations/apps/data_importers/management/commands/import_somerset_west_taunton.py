from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "SWT"
    addresses_name = "2024-07-04/2024-06-17T16:33:01.558703/Eros_SQL_Output012.csv"
    stations_name = "2024-07-04/2024-06-17T16:33:01.558703/Eros_SQL_Output012.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093895310",  # KILTON COTTAGES, 11 KILTON, HOLFORD, BRIDGWATER
            "10014267234",  # MOONBEAMS FARM, WELLINGTON
            "10008798191",  # PIXFORD FARM, BISHOPS LYDEARD, TAUNTON
            "10008799902",  # HIGHER BARN PIXFORD FRUIT FARM RALEIGHS CROSS ROAD, COMBE FLOREY, TAUNTON
            "10008799901",  # ROSE COTTAGE, KILTON, HOLFORD, BRIDGWATER
            "100041178433",  # SLADE TOWER, EIGHT ACRE LANE, WELLINGTON
            "100040957626",  # AYSGARTH, BOSSINGTON LANE, PORLOCK, MINEHEAD
            "10094760892",  # FLAT AT DENTCARE LAB MIDDLE STREET, MINEHEAD
            "200003159845",  # LOWERCOT, MART ROAD, MINEHEAD
            "10003765832",  # THE BUNGALOW, DRAGONS CROSS, BILBROOK, MINEHEAD
            "100040965076",  # 28 TOWER HILL, WILLITON, TAUNTON
            "100040965037",  # 25 TOWER HILL, WILLITON, TAUNTON
            "10023836664",  # BEGGARS ROOST, LILSTOCK, BRIDGWATER
            "10003764036",  # ROSE COTTAGE, KILTON, HOLFORD, BRIDGWATER
            "10003766053",  # KILTON COTTAGES, 11 KILTON, HOLFORD, BRIDGWATER
            "10003764306",  # KWETU, HOLFORD, BRIDGWATER
            "10003764307",  # COREWELL FARM, HOLFORD, BRIDGWATER
            "10014261828",  # PARK COTTAGE, TRISCOMBE, BISHOPS LYDEARD, TAUNTON
            "10003561439",  # KEEPERS COTTAGE, TRISCOMBE, BISHOPS LYDEARD, TAUNTON
            "100040932552",  # AVALON, LANGFORD LANE, PEN ELM, TAUNTON
            "10008800843",  # STABLE COTTAGE FOXHOUND KENNELS, THORNFALCON, TAUNTON
            "10008797250",  # MONTGOMERY COTTAGE ADCOMBE LANE, CORFE, TAUNTON
            "10008801166",  # HAYNE, CORFE, TAUNTON
            "10014261283",  # CHELSTON PARK NURSING HOME, CHELSTON, WELLINGTON
            "10002704635",  # CADESIDE CARAVAN & MOTORHOME CLUB SITE, POOLE, WELLINGTON
            "10093895345",  # THE STABLES, HENLADE, TAUNTON
            "10008798445",  # SAMPFORD GATE, SAMPFORD ARUNDEL, WELLINGTON
            "100040943537",  # AGINGHILLS FARM, SWINGBRIDGE, BATHPOOL, TAUNTON
            "10014264578",  # THE ANNEXE AGINHILLS FARM SWINGBRIDGE, BATHPOOL, TAUNTON
            "200003157166",  # HIGHER ELLICOMBE, ELLICOMBE, MINEHEAD
            "10003560984",  # CROSSWAYS FARM, BILBROOK, MINEHEAD
            "10003763552",  # CLITSOME FARM, ROADWATER, WATCHET
            "10003764816",  # MOORSIDE BUNGALOW, WOOLSTON, WILLITON, TAUNTON
            "10093574538",  # LOWER THORNES HOUSE, WOOLSTON, WILLITON, TAUNTON
            "10002701877",  # LUXBOROUGH FARM, AISHOLT, BRIDGWATER
            "10002698863",  # WATERHOUSE FARM, PICKNEY, KINGSTON ST. MARY, TAUNTON
            "100040932119",  # OKEHILLS, KINGSTON ROAD, TAUNTON
            "10008799362",  # ALLERFORD INN, NORTON FITZWARREN, TAUNTON
            "10095821552",  # 3 MERTON WALK, RUMWELL, TAUNTON
            "10002700125",  # HILLBROOK, DIPFORD ROAD, TRULL, TAUNTON
            "100041070307",  # 42 EAST STREET, TAUNTON
            "10003766281",  # MACHINE COURT, DULVERTON
            "10008797522",  # ROUNDHILL, BRADFORD ON TONE, TAUNTON
            "10004117133",  # 12A MIDDLE STREET, TAUNTON
            "10008800166",  # BLACKWELL FARM, RADDINGTON, TAUNTON
            "10003764756",  # TARR STEPS FARM, DULVERTON
            "10095820192",  # THE OLD TRACTOR SHED, DULVERTON
            "10023836286",  # MARSHWOOD, EXTON, DULVERTON
            "10003764682",  # SPRINGHAYES, EXTON, DULVERTON
            "10004117133",  # 12A MIDDLE STREET, TAUNTON
            "100041070305",  # H&R SALON, 40 EAST STREET, TAUNTON
            "10003560798",  # LEAT HOUSE, TORRE FISHERIES, TORRE, WASHFORD, WATCHET
            "10002703431",  # NOWERS FARM, NOWERS LANE, WELLINGTON
            "10095822782",  # SCARLET ELF, TRACEBRIDGE, ASHBRITTLE, WELLINGTON
            "10003561423",  # ORCHARDBROOK, WASHFORD, WATCHET
            "10008802488",  # 1 ORCHARD VIEW, RUMWELL, TAUNTON
            "10008801747",  # 2 ORCHARD VIEW, RUMWELL, TAUNTON
            "10008798251",  # HOCCOMBE FORD FARM, LYDEARD ST. LAWRENCE, TAUNTON
        ]:
            return None

        if record.housepostcode in [
            # splits
            "TA3 5FE",
            "TA23 0ED",
            "TA23 0BG",
            "TA2 7ED",
            "TA23 0TX",
            "TA2 8NZ",
            "TA24 6TE",
            "TA23 0NX",
            "TA24 5QF",
            # looks wrong
            "TA24 8AB",
            "TA23 0NS",
            "TA2 8RB",
            "TA21 0HE",
            "TA21 0HB",
            "TA3 7AQ",
            "TA3 7BL",
            "TA3 7BW",
            "TA24 7JY",
            "TA23 0RR",
            "TA4 4JE",
            "TA24 5UR",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # more accurate location for: Williams Hall Dark Lane Stoke St Gregory Taunton TA3 6HA
        if record.pollingstationname == "Williams Hall":
            rec["location"] = Point(-2.930735, 51.041830, srid=4326)

        # more accurate location for: Victoria Park Pavilion Victoria Gate Taunton TA1 3ES
        if record.pollingstationname == "Victoria Park Pavilion":
            rec["location"] = Point(-3.091746, 51.017816, srid=4326)
        return rec
