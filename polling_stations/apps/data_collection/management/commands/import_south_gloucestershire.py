from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000025"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019sglo.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019sglo.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "569728",  # BS352LG -> BS353LG : Hillrise, Thornbury Road, Alveston, Bristol
            "677349",  # BS351BP -> BS352HQ : Orchard Cottage, Knapp Road, Thornbury, Bristol
            "624155",  # BS305NH -> BS305NL : 1 Cann Farm, Cann Lane, Warmley, Bristol
            "624157",  # BS305NH -> BS305NL : 2 Cann Farm, Cann Lane, Warmley, Bristol
            "554011",  # BS378QP -> BS378QH : Leas End, Westerleigh Road, Westerleigh, Bristol
            "583982",  # BA18HD -> BA18HQ : Henley Tyning Farm, St Catherines, Bath
            "553985",  # BS378QP -> BS378QH : Nelson Cottage, Westerleigh Road, Westerleigh, Bristol
            "553987",  # BS378QP -> BS378QH : Sunnyside Bungalow, Westerleigh Road, Westerleigh, Bristol
            "622223",  # BS166PX -> BS166TB : Baugh Cottage, Off Bury Hill View, Downend, Bristol
            "577950",  # BS375JG -> BS375JH : Nibley Mill Bungalow, Hope Road, Yate, Bristol
            "651973",  # BS378QH -> BS378QG : Bridge View Mobile Home, Westerleigh Road, Coalpit Heath, Bristol
            "555377",  # BS324AH -> BS324AR : Amberley House, Hempton Lane, Almondsbury, Bristol
            "578656",  # BS351RL -> BS351RN : 2 Knights View, Shepperdine Road, Oldbury-on-Severn, Bristol
            "625229",  # BS351RL -> BS351RN : 1 Knights View, Shepperdine Road, Oldbury-on-Severn, Bristol
            "581915",  # GL139EA -> GL139DZ : Knightsleaze, Hill, Berkeley, Gloucester
            "582152",  # GL128PX -> GL128PU : Yew Tree Bungalow, Horseshoe Hill, Milbury Heath, Wotton Under Edge
            "641051",  # GL128DY -> GL128QL : The Cottage, Whitewall Lane Buckover, Wotton Under Edge, Gloucestershire
            "581876",  # BS351LF -> BS351LB : Hill Crest, Lower Morton, Thornbury, Bristol
            "528682",  # BS154HN -> BS154HJ : 47 Honey Hill Road, Kingswood, Bristol
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "509039",  # BS347ET -> BS377DY : 12 Charles Road, Filton, Bristol
        ]:
            rec["accept_suggestion"] = False

        return rec
