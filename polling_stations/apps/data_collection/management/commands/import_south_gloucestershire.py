from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000025"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019SGlos.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019SGlos.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "679205":
            rec["postcode"] = "BS161PF"
            rec["accept_suggestion"] = False

        if uprn == "605413":  # SN148DB -> SN148LX
            rec["postcode"] = "SN148LX"
            rec["accept_suggestion"] = False

        if uprn == "653347":  # BS78QN -> BS70QN
            rec["postcode"] = "BS70QN"
            rec["accept_suggestion"] = False

        if uprn == "648155":  # BS107RQ -> BS107RQ
            rec["postcode"] = "BS107RQ"
            rec["accept_suggestion"] = False

        if uprn in [
            "624155",  # BS305NH -> BS305NL : 1 Cann Farm, Cann Lane, Warmley, Bristol
            "624157",  # BS305NH -> BS305NL : 2 Cann Farm, Cann Lane, Warmley, Bristol
            "554011",  # BS378QP -> BS378QH : Leas End, Westerleigh Road, Westerleigh, Bristol
            "583982",  # BA18HD -> BA18HQ : Henley Tyning Farm, St Catherines, Bath
            "553985",  # BS378QP -> BS378QH : Nelson Cottage, Westerleigh Road, Westerleigh, Bristol
            "553987",  # BS378QP -> BS378QH : Sunnyside Bungalow, Westerleigh Road, Westerleigh, Bristol
            "641633",  # BS376QA -> BS376PX : The Lodge, Little Sodbury Manor, Little Sodbury, Chipping Sodbury, Bristol
            "622223",  # BS166PX -> BS166TB : Baugh Cottage, Off Bury Hill View, Downend, Bristol
            "577950",  # BS375JG -> BS375JH : Nibley Mill Bungalow, Hope Road, Yate, Bristol
            "651973",  # BS378QH -> BS378QG : Bridge View Mobile Home, Westerleigh Road, Coalpit Heath, Bristol
            "555377",  # BS324AH -> BS324AR : Amberley House, Hempton Lane, Almondsbury, Bristol
            "556973",  # BS354AQ -> BS354AH : Haywood Cottage, Camp Lane, Elberton, Olveston, Bristol
            "582188",  # BS351NR -> BS351NL : Silverhill, Littleton on Severn, Bristol
            "578656",  # BS351RL -> BS351RN : 2 Knights View, Shepperdine Road, Oldbury-on-Severn, Bristol
            "625229",  # BS351RL -> BS351RN : 1 Knights View, Shepperdine Road, Oldbury-on-Severn, Bristol
            "581915",  # GL139EA -> GL139DZ : Knightsleaze, Hill, Berkeley, Gloucester
            "582152",  # GL128PX -> GL128PU : Yew Tree Bungalow, Horseshoe Hill, Milbury Heath, Wotton Under Edge, Gloucestershire
            "641051",  # GL128DY -> GL128QL : The Cottage, Whitewall Lane Buckover, Wotton Under Edge, Gloucestershire
            "581876",  # BS351LF -> BS351LB : Hill Crest, Lower Morton, Thornbury, Bristol
            "528682",  # BS154HN -> BS154HJ : 47 Honey Hill Road, Kingswood, Bristol
        ]:

            rec["accept_suggestion"] = True

        return rec
