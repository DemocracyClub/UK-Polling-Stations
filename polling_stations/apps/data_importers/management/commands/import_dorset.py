from django.contrib.gis.geos import Point

from addressbase.models import Address
from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


CORRECTIONS = {
    "39064": {
        "address": "Larksmead Pavilion - Station 1,Larksmead,Blandford Forum",
        "uprn": "10013291376",
        "postcode": "DT11 7GF",
    },
    "39433": {
        "address": "Durweston Village Hall,Durweston",
        "uprn": "10013273822",
        "postcode": "DT11 0QA",
    },
    "39823": {
        "address": "Spetisbury Village Hall,Spetisbury",
        "uprn": "10013293549",
        "postcode": "DT11 9DT",
    },
    "38932": {
        "address": "Milton Abbas Reading Room,Milton Abbas",
        "uprn": "10013296099",
        "postcode": "DT11 0BN",
    },
    "39430": {
        "address": "Child Okeford Village Hall,Child Okeford",
        "uprn": "100041047771",
        "postcode": "DT11 8EX",
    },
    "39538": {
        "address": "Winterborne Zelston Village Hall,Winterborne Zelston",
        "uprn": "10013296129",
        "postcode": "DT11 9EU",
    },
    "39381": {
        "address": "Bourton Village Hall,Bourton",
        "uprn": "10013220033",
        "postcode": "SP8 5BJ",
    },
    "39555": {
        "address": "Winterborne Whitechurch Village Hall,Winterborne Whitechurch",
        "uprn": "10013297777",
        "postcode": "DT11 0AW",
    },
    "39410": {
        "address": "Gillingham Town Hall (Council Chamber),School Road,Gillingham,Dorset",
        "uprn": "200002927650",
        "postcode": "SP8 4QR",
    },
    "39394": {
        "address": "Buckhorn Weston Village Hall,Buckhorn Weston",
        "uprn": "10013296158",
        "postcode": "SP8 5HF",
    },
    "39388": {
        "address": "Kington Magna Village Hall,Kington Magna",
        "uprn": "10013296189",
        "postcode": "SP8 5EW",
    },
    "39733": {
        "address": "Hinton St Mary Village Hall,Hinton St Mary,Hinton St Mary,Sturminster Newton",
        "uprn": "10013291636",
        "postcode": "DT10 1NA",
    },
    "39704": {
        "address": "Stourton Caundle Village Hall,Stourton Caundle",
        "uprn": "10013296205",
        "postcode": "DT10 2JN",
    },
    "39371": {
        "address": "Longham United Reformed Church Hall,Longham",
        "uprn": "200002908652",
        "postcode": "BH22 9AW",
    },
    "39378": {
        "address": "St. Mary`s Church Hall,Church Road,Ferndown,Dorset",
        "uprn": "100041101507",
        "postcode": "BH22 9EU",
    },
    "39235": {
        "address": "Alderholt Village Hall,Station Road,Alderholt",
        "uprn": "10002931696",
        "postcode": "SP6 3RB",
    },
    "39830": {
        "address": "Three Legged Cross Village Hall,Three Legged Cross",
        "uprn": "100041050956",
        "postcode": "BH21 6SG",
    },
    "39272": {
        "address": "Pentridge Village Hall,Pentridge",
        "uprn": "10002929771",
        "postcode": "SP5 5QX",
    },
    "39725": {
        "address": "Sturminster Marshall Memorial Hall,Churchill Close,Sturminster Marshall,Wimborne",
        "uprn": "100041051034",
        "postcode": "BH21 4BQ",
    },
    "39239": {
        "address": "Cecil Memorial Hall,Cranborne,Cranborne,Wimborne",
        "uprn": "100041050515",
        "postcode": "BH21 5QB",
    },
    "39242": {
        "address": "Edmondsham Village Hall,Edmondsham",
        "uprn": "10002928992",
        "postcode": "BH21 5RG",
    },
    "39268": {
        "address": "Gussage All Saints Village Hall,Gussage All Saints",
        "uprn": "10002946450",
        "postcode": "BH21 5ET",
    },
    "39246": {
        "address": "Wimborne St Giles Village Hall,Wimborne St Giles",
        "uprn": "10002925538",
        "postcode": "BH21 5LX",
    },
    "39693": {
        "address": "St Leonards & St Ives Village Hall,Braeside Road,St Leonards,Ringwood,Hants",
        "uprn": "100041051002",
        "postcode": "BH24 2PH",
    },
    "39935": {
        "address": "Halstock Community Hall,Leigh Lane,BA22 9SG",
        "uprn": "200000747353",
        "postcode": "BA22 9SH",
    },
    "39484": {
        "address": "Lytchett Minster Rugby Club,Old Watery Lane,Lytchett Minster,BH16 6JE",
        "uprn": "10013730190",
        "postcode": "BH16 6HZ",
    },
    "40048": {
        "address": "Herston Hall - Station 2,Jubilee Road,Swanage,BH19 2SE",
        "uprn": "100041096534",
        "postcode": "BH19 2SF",
    },
    "39746": {
        "address": "Herston Hall - Station 1,Jubilee Road,Swanage,BH19 2SE",
        "uprn": "100041096534",
        "postcode": "BH19 2SF",
    },
    "39596": {
        "address": "Studland Village Hall,Heathgreen Road,Studland,Swanage,BH19 3BT",
        "uprn": "100041097058",
        "postcode": "BH19 3BX",
    },
    "39588": {
        "address": "Furzebrook Village Hall,Furzebrook,Wareham,BH20 4AR",
        "uprn": "100041048955",
        "postcode": "BH20 5AR",
    },
    "39769": {
        "address": "Carey Hall - Station 1,Mistover Road,Wareham,BH20 4BA",
        "uprn": "200004825078",
        "postcode": "BH20 4BY",
    },
    "40032": {
        "address": "Carey Hall - Station 2,Mistover Road,Wareham,BH20 4BA",
        "uprn": "200004825078",
        "postcode": "BH20 4BY",
    },
    "38921": {
        "address": "Stoborough Village Hall,Stoborough,Wareham,BH20 5AD",
        "uprn": "200004827814",
        "postcode": "BH20 5DA",
    },
    "39219": {
        "address": "Colehill Memorial Hall - Station 3,Cannon Hill Road,Colehill,Wimborne,BH21 2LR",
        "uprn": "100041100240",
        "postcode": "BH21 2LS",
    },
    "39218": {
        "address": "Colehill Memorial Hall - Station 2,Cannon Hill Road,Colehill,Wimborne,BH21 2LR",
        "uprn": "100041100240",
        "postcode": "BH21 2LS",
    },
    "39213": {
        "address": "Colehill Memorial Hall - Station 1,Cannon Hill Road,Colehill,Wimborne,BH21 2LR",
        "uprn": "100041100240",
        "postcode": "BH21 2LS",
    },
    "39715": {
        "address": "Holt Parish Hall,Holt Lane,Holt,Wimborne,BH21 7DQ",
        "uprn": "10002925948",
        "postcode": "BH21 7DH",
    },
    "39833": {
        "address": "West Moors Memorial Hall - Station 1,Station Road,West Moors,Ferndown,BH22 0HS",
        "uprn": "100041101073",
        "postcode": "BH22 0HZ",
    },
    "39836": {
        "address": "West Moors Memorial Hall - Station 2,Station Road,West Moors,Ferndown,BH22 0HS",
        "uprn": "100041101073",
        "postcode": "BH22 0HZ",
    },
    "40050": {
        "address": "Weymouth Avenue Cricket Pavilion - Station 2,Recreation Ground,Dorchester,DT1 2RY",
        "uprn": "10093508518",
        "postcode": "DT1 2RZ",
    },
    "39302": {
        "address": "Weymouth Avenue Cricket Pavilion - Station 1,Recreation Ground,Dorchester,DT1 2RY",
        "uprn": "10093508518",
        "postcode": "DT1 2RZ",
    },
    "38998": {
        "address": "Manston Village Hall,Manston,DT10 1EY",
        "uprn": "10013291292",
        "postcode": "DT10 1HB",
    },
    "40065": {
        "address": "Chivrick Room - Station 2,The Exchange,Old Market Hill,Sturminster Newton,DT10 1QU",
        "uprn": "10013289840",
        "postcode": "DT10 1FH",
    },
    "39044": {
        "address": "Ibberton Village Hall,Ibberton,DT11 0EL",
        "uprn": "10013291331",
        "postcode": "DT11 0EN",
    },
    "39549": {
        "address": "Committee Room,Milborne St Andrew Village Hall,Milborne St Andrew,DT11 0JB",
        "uprn": "10013294039",
        "postcode": "DT11 0JX",
    },
    "39014": {
        "address": "Sutton Waldron Village Hall,Sutton Waldron,DT11 8NZ",
        "uprn": "10013273855",
        "postcode": "DT11 8NZ",
    },
    "39437": {
        "address": "Pimperne Village Hall,Newfield Road,Pimperne,DT11 8WF",
        "uprn": "10013296101",
        "postcode": "DT11 8WF",
    },
    "39261": {
        "address": "Tarrant Keyneston Village Hall,Tarrant Keyneston,DT11 9JE",
        "uprn": "10013283491",
        "postcode": "DT11 9JB",
    },
    "39352": {
        "address": "Toller Porcorum Village Hall (Committee Room),Church Mead,DT2 0DE",
        "uprn": "10023242882",
        "postcode": "DT2 0DT",
    },
    "39850": {
        "address": "Briantspuddle Village Hall (Diamond Jubilee Room),Briantspuddle,Dorchester,DT2 7HT",
        "uprn": "10013729688",
        "postcode": "DT2 7HS",
    },
    "39878": {
        "address": "East Chaldon Village Hall,East Chaldon,Dorchester,DT2 8DL",
        "uprn": "10011954429",
        "postcode": "DT2 8DN",
    },
    "39884": {
        "address": "Moreton Village Hall (Stage Room),Moreton,Dorchester,DT2 8RD",
        "uprn": "10013733148",
        "postcode": "DT2 8RE",
    },
    "39542": {
        "address": "Puddletown Village Hall,High Street,DT2 8RX",
        "uprn": "100041033137",
        "postcode": "DT2 8RY",
    },
    "40038": {
        "address": "Radipole URC Church Hall - Station 2,Roman Road,Radipole,Weymouth,DT3 5JQ",
        "uprn": "10070568857",
        "postcode": "DT3 5EN",
    },
    "39559": {
        "address": "Radipole URC Church Hall - Station 1,Roman Road,Radipole,Weymouth,DT3 5JQ",
        "uprn": "10070568857",
        "postcode": "DT3 5EN",
    },
    "39448": {
        "address": "Littlemoor Community Centre,Canberra Road,Weymouth,DT3 6AY",
        "uprn": "10070567648",
        "postcode": "DT3 6AY",
    },
    "39284": {
        "address": "Osmington Village Hall (Main Hall),Shortlake Lane,DT3 6EG",
        "uprn": "10023242897",
        "postcode": "DT3 6FT",
    },
    "39455": {
        "address": "Preston Village Hall,Preston Road,Preston,Weymouth,DT3 8BH",
        "uprn": "100041118323",
        "postcode": "DT3 6BH",
    },
    "39568": {
        "address": "Westham Methodist Church Hall,Milton Road,Weymouth,DT4 9DL",
        "uprn": "100041118873",
        "postcode": "DT4 9DL",
    },
    "38958": {
        "address": "Weston Community Hall,Weston Road,Portland,DT5 2DA",
        "uprn": "100041049367",
        "postcode": "DT5 2BZ",
    },
    "39090": {
        "address": "The Salt House,Quayside,West Bay,DT6 4EN",
        "uprn": "10013011777",
        "postcode": "DT6 4HD",
    },
    "39134": {
        "address": "Burton Bradstock Village Hall,Church Street,DT6 4QF",
        "uprn": "200000757539",
        "postcode": "DT6 4QS",
    },
    "40145": {
        "address": "Hunts Supermarket,Digby Road,Sherborne,DT9 3NW",
        "uprn": "100041122784",
        "postcode": "DT9 3GF",
    },
    "39276": {
        "address": "Sixpenny Handley Village Hall,Sixpenny Handley,Common Lane,Nr Salisbury,SP5 5NH",
        "uprn": "100041169780",
        "postcode": "SP5 5NJ",
    },
    "39002": {
        "address": "Fontmell Magna Village Hall,Fontmell Magna,SP7 0PS",
        "uprn": "10013296165",
        "postcode": "SP7 0JP",
    },
}


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "DOR"
    addresses_name = "2021-03-04T13:35:03.539800/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-04T13:35:03.539800/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if "NEW LOCATION" in record.polling_place_name:
            record = record._replace(polling_place_name="")

        # If we have a correction, use it.
        if record.polling_place_id in CORRECTIONS:
            record = record._replace(
                polling_place_postcode=CORRECTIONS[record.polling_place_id]["postcode"]
            )
            record = record._replace(
                polling_place_uprn=CORRECTIONS[record.polling_place_id]["uprn"]
            )
        # if not see if the uprn is in addressbase, if it is, use it, if not bin it.
        elif record.polling_place_uprn:
            try:
                addressbase_record = Address.objects.get(uprn=record.polling_place_uprn)
                record = record._replace(
                    polling_place_postcode=addressbase_record.postcode
                )
            except Address.DoesNotExist:
                record = record._replace(polling_place_uprn="")

        # Allendale House
        # user issue report #39
        if record.polling_place_id == "39802":
            record = record._replace(polling_place_uprn="100041099964")

        rec = super().station_record_to_dict(record)

        # Portesham Village Hall
        # user issue report #38
        if record.polling_place_id == "39123":
            rec["location"] = Point(-2.567644, 50.668385, srid=4326)
            return rec

        # Bishops Caundle Village Hall
        # user issue report #40
        if record.polling_place_id == "39641":
            rec["location"] = Point(-2.437757, 50.915554, srid=4326)
            return rec

        # All Saints Church Hall
        # user issue report #41
        if record.polling_place_id in ["39684", "39688"]:
            rec["location"] = Point(-1.834570, 50.831005, srid=4326)
            return rec

        # St Marys Church Hall
        if record.polling_place_id == "35117":
            rec["location"] = Point(-2.443608, 50.709373, srid=4326)
            return rec

        # Southill Community Centre
        # user issue report #47
        if record.polling_place_id == "39562":
            rec["location"] = Point(-2.477398, 50.623534, srid=4326)
            return rec

        # Moose Lodge
        # user issue report #43
        if record.polling_place_id == "39576":
            rec["location"] = Point(-2.466883, 50.606307, srid=4326)
            return rec

        # Charlton Marshall Parish Centre
        if record.polling_place_id == "39819":
            rec["location"] = Point(-2.14121, 50.83429, srid=4326)
            return rec

        # West Moors Memorial Hall
        # user issue report #132
        if record.polling_place_id in ["39836", "39833"]:
            rec["location"] = Point(-1.89013, 50.82904, srid=4326)
            return rec

        # Dorset Fire & Rescue, Peverell Avenue West...
        if record.polling_place_id == "35112":
            rec["location"] = Point(-2.471750, 50.713013, srid=4326)
            return rec

        # Furzebrook Village Hall
        if record.polling_place_id == "34895":
            rec["location"] = Point(-2.10060, 50.65811, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() in [
            "DT4 0BA",
            "DT4 7QN",
            "DT3 6SD",
            "DT6 4QH",
            "DT6 6EU",
            "DT6 4LD",
            "DT2 0JE",
            "DT9 5FP",
            "DT2 8DX",
            "SP7 8RE",
            "SP8 4AL",
            "SP8 4DG",
            "DT10 1HG",
            "DT10 1QZ",
            "BH21 7LY",
            "BH21 7BG",
            "BH21 2DE",
            "BH31 6PA",
            "BH21 3NF",
            "BH21 4AD",
            "BH31 6EH",
            "BH31 6QG",
            "BH21 5NP",
            "BH21 5JD",
            "BH21 4JU",
            "BH19 2PG",
            "BH20 5JJ",
            "BH20 4BJ",
            "BH20 5PT",
            "DT11 7AR",
            "DT2 8GD",
            "DT2 8GD",
        ]:
            return None

        if uprn in [
            "100040620232",  # THE OLD CIDER PRESS, EAST STREET, BEAMINSTER
            "100041048946",  # 21A EAST STREET, CORFE CASTLE, WAREHAM
            "10013731266",  # FLAT 2 PURBECK LODGE 15 BONNETS LANE, WAREHAM
            "10013731265",  # FLAT 1 PURBECK LODGE 15 BONNETS LANE, WAREHAM
        ]:
            return None

        return super().address_record_to_dict(record)
