from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from pollingstations.models import PollingStation
from addressbase.models import Address


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2026-05-07/2026-04-20T12:03:38.549959/Updated Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-04-20T12:03:38.549959/Updated Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Community Suite, Llanishen Leisure Centre, Ty Glas Avenue, Llanishen, Cardiff
        if record.polling_place_id == "25858":
            # geocode was a way off, postcode was right, but found the building so here it is anyway
            record = record._replace(polling_place_uprn="10002526454")

        # The Church Hall, Kelston Road, Whitchurch, Cardiff
        if record.polling_place_id == "21205":
            record = record._replace(polling_place_uprn="200001850852")

        # St Mary`s Church Hall, Church Road, Cardiff, CF14 2ED
        # Council request to use below postcode, ignore the warning
        if record.polling_place_id == "25906":
            record = record._replace(
                polling_place_postcode="CF14 2DX", polling_place_uprn="10008903814"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100100110392",  # 10 SOMERSET COURT, BURNHAM AVENUE, LLANRUMNEY, CARDIFF
            "10008904957",  # OAK HOUSE, 340 NEWPORT ROAD, CARDIFF
            "10090488749",  # 456A COWBRIDGE ROAD EAST, CARDIFF
            "10092985344",  # FIRST FLOOR FLAT 452 COWBRIDGE ROAD EAST, CANTON, CARDIFF
            "10002507423",  # MAES Y LLECH FARM, RADYR, CARDIFF
            "100100896720",  # PARK HOUSE, MUIRTON ROAD, CARDIFF
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CF24 2DG",
            # looks wrong
            "CF11 6BN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def post_import(self):
        # The a117 data the councils sent had UPRNs for polling stations that weren't in the EMS data
        a11y_uprns = {
            "25673": 200001850808,
            "25678": 100101042723,
            "25681": 100100896159,
            "25684": 10008904146,
            "25687": 10008904139,
            "25690": 10013745626,
            "25693": 10008903793,
            "25697": 200001850823,
            "25702": 200002934557,
            "25705": 10002509036,
            "25708": 10090717759,
            "25711": 10023543872,
            "25714": 10008903878,
            "25717": 10008903875,
            "25720": 10003567591,
            "25723": 10008903759,
            "25726": 200002933723,
            "25729": 10013745044,
            "25732": 10092985401,
            "25735": 10002508283,
            "25738": 10090489727,
            "25741": 100101042585,
            "25744": 200001861442,
            "25747": 10092989608,
            "25750": 200001679329,
            "25753": 10008903873,
            "25756": 200002934222,
            "25759": 10002506628,
            "25762": 200002934087,
            "25765": 100101041995,
            "25769": 10008903798,
            "25774": 10095458804,
            "25777": 100101042595,
            "25779": 100100898986,
            "25782": 10002509641,
            "25785": 10008904449,
            "25788": 100101041915,
            "25791": 100101042234,
            "25794": 10008905578,
            "25797": 100101042837,
            "25801": 10023549575,
            "25804": 100100893566,
            "25807": 100100893486,
            "25810": 200001878036,
            "25813": 10008903866,
            "25816": 200002932867,
            "25819": 10008904152,
            "25822": 100101043413,
            "25825": 10008905224,
            "25828": 100101042466,
            "25831": 10002506001,
            "25834": 10002529560,
            "25837": 200002932765,
            "25841": 10002526487,
            "25847": 200002932749,
            "25850": 10023550280,
            "25853": 100101043581,
            "25861": 10008903863,
            "25864": 10090717921,
            "25870": 10008903892,
            "25873": 10003567458,
            "25876": 10008903889,
            "25882": 200001850865,
            "25888": 10002527528,
            "25891": 10013746170,
            "25894": 200002933008,
            "25897": 200001846297,
            "25900": 10002527501,
            "25903": 200001850852,
            "25909": 10008903752,
            "25913": 100101042673,
            "25916": 10002520655,
            "25934": 10002506984,
            "25941": 10013748118,
            "25944": 200002932059,
            "25948": 10095462047,
            "25951": 10090719775,
            "25954": 200002934221,
            "25958": 200002934193,
            "25961": 200002934212,
            "25965": 200002934212,
            "25968": 10013085989,
            "25972": 200002932233,
            "25975": 100101043388,
            "25978": 10013745018,
            "25981": 10008904116,
            "25984": 10002527732,
            "25988": 200002932211,
            "25991": 200002933945,
            "25994": 100101043383,
            "25997": 200002934014,
            "26000": 10008904156,
            "26004": 100101043395,
            "26007": 10090487710,
            "26010": 10002526456,
            "26011": 200002934022,
            "26016": 10002508100,
            "26019": 10002508130,
            "26022": 10023549988,
            "26026": 200002938936,
            "26029": 10003567926,
            "26032": 10090717987,
            "26035": 10013745045,
            "26038": 200002938658,
            "26041": 10023546496,
            "26044": 200002938839,
            "26047": 200002938935,
            "26050": 100100915690,
            "26053": 200001680063,
            "26056": 10008903830,
            "26062": 10008903787,
            "26065": 10090719816,
            "26070": 10002516892,
            "26073": 10002525523,
            "26076": 10002527328,
            "26079": 200002938793,
            "26083": 10008903826,
            "26086": 10023550997,
            "26089": 200001850885,
            "26092": 10093728732,
            "26095": 10002525421,
            "26098": 10002527771,
            "26101": 10003563021,
            "26104": 10013083385,
            "26107": 10002509007,
            "26111": 10002518407,
            "26114": 10002526437,
            "26117": 10008903758,
            "26120": 10008903756,
            "26123": 10008903848,
            "26126": 200002932521,
            "26129": 10008903799,
            "26135": 10096553509,
            "26138": 200002932225,
            "26141": 10002528880,
            "26144": 200002932223,
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
