from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E06000059"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019dorset.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019dorset.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_4",
        "polling_place_address_3",
        "polling_place_address_2",
    ]

    def station_record_to_dict(self, record):

        if record.polling_place_id in ["30165", "30169"]:
            record = record._replace(polling_place_postcode="")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.017478, 50.774375, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100040697695":
            rec["postcode"] = "BH31 7DB"

        if record.addressline6.strip() == "DT4 OTU":
            rec["postcode"] = "DT4 0TU"

        if uprn == "10071151515":
            rec["postcode"] = "SP7 9NS"

        if uprn == "10013274889":
            rec["postcode"] = "SP7 9PH"

        if record.addressline6.strip() in ["DT2 7QF", "DT8 3DS"]:
            return None

        if uprn in ["10023251279", "100041048946", "10013297602"]:
            return None

        if uprn in ["10013731265", "10013731266"]:
            rec["postcode"] = "BH20 4HA"
            rec["accept_suggestion"] = False

        if record.addressline1.strip() == "Chalet 7 Seaview Holiday Park":
            return None

        if uprn in [
            "10023242559",  # DT27HW -> DT29HW : Maybyrne, Long Bredy, Dorchester, Dorset
            "100040710093",  # BH216LJ -> BH218LJ : Silver Trees, Verwood Road, Woodlands, Wimborne, Dorset
            "10002640153",  # DT28HW -> DT28NJ : Seafield, Holworth, Dorchester, Dorset
            "10013274894",  # SP85RE -> SP84RE : Flat 1, The Stables, Horkesley Hall Farm, Common Mead Lane, Gillingham
            "10013286779",  # SP85RE -> SP84RE : Flat 2, The Stables, Horkesley Hall Farm, Common Mead Lane, Gillingham
            "200004827271",  # BH214AD -> BH214AB : South Oak, Dullar Farm, Dullar Farm Lane, Sturminster Marshall
            "200004827507",  # BH166BA -> BH166BB : 13 Race Farm Cottages, Huntick Road, Lytchett Minster
            "10002063437",  # DT51LP -> DT51LX : Middle Flat, 69 Fortuneswell, Portland, Dorset
            "10002945632",  # BH214JT -> BH214JQ : Bryngorwen Cottage, Petersham Lane, Gaunts, Wimborne, Dorset
            "10023250759",  # DT65JR -> DT65JT : The Dairy House Vearse Farm, West Road, Bridport, Dorset
            "10023250758",  # DT65JR -> DT65JT : Vearse Farmhouse, West Road, Bridport, Dorset
            "100040700552",  # BH217JT -> BH217JX : Windy Ridge Burts Lane, Mannington, Horton Heath, Wimborne, Dorset
            "10011953652",  # BH191LT -> BH191LS : Flat 1 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953653",  # BH191LT -> BH191LS : Flat 2 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953654",  # BH191LT -> BH191LS : Flat 3 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953655",  # BH191LT -> BH191LS : Flat 4 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953656",  # BH191LT -> BH191LS : Flat 5 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953657",  # BH191LT -> BH191LS : Penthouse 1 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953658",  # BH191LT -> BH191LS : Penthouse 2 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953659",  # BH191LT -> BH191LS : Penthouse 3 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "200004744859",  # BH316PU -> BH317LG : St.Margarets, Brickyard Lane, Verwood, Dorset
            "100040657448",  # DT40LY -> DT40JY : Flat 2, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657451",  # DT40LY -> DT40JY : Flat 5, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657452",  # DT40LY -> DT40JY : Flat 6, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657453",  # DT40LY -> DT40JY : Flat 7, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657450",  # DT40LY -> DT40JY : Flat 4, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657449",  # DT40LY -> DT40JY : Flat 3, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "10002058413",  # DT40GU -> DT40QU : Flat 2, 307 Chickerell Road, Weymouth, Dorset
            "10002058412",  # DT40GU -> DT40QU : Flat 1, 307 Chickerell Road, Weymouth, Dorset
            "200000766574",  # DT83HY -> DT83HX : Wayland Farm, Chedington, Beaminster, Dorset
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200000767829",  # DT65BJ -> DT65BL : Caretaker`s Flat Boldwood House, 13 West Allington, Bridport, Dorset
            "100040700422",  # BH213RB -> BH213RA : 2 Meadow View, Broadmoor Road, Corfe Mullen, Wimborne, Dorset
            "100040700541",  # BH217JX -> BH217JT : High Trees Burts Lane, Mannington, Horton Heath, Wimborne, Dorset
            "100040700546",  # BH217JX -> BH217JT : Rose Cottage Farm Burts Lane, Mannington, Horton Heath, Wimborne, Dorset
        ]:
            rec["accept_suggestion"] = False

        return rec
