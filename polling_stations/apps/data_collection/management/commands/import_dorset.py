from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000059"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    # There have been a lot of fixes, so try letting rest through.
    allow_station_point_from_postcode = True

    def station_record_to_dict(self, record):

        # Allendale House
        # user issue report #39
        if record.polling_place_id == "34414":
            record = record._replace(polling_place_uprn="100041099964")

        # last-minute change for parl.2019-12-12
        # https://trello.com/c/Ij4tgMP1
        if record.polling_place_id == "35139":
            record = record._replace(polling_place_name="The Parish Pavilion")
            record = record._replace(polling_place_address_1="Buckland Newton")
            record = record._replace(polling_place_address_2="Dorchester")
            record = record._replace(polling_place_address_3="Dorset")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="DT2 7DP")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            rec = super().station_record_to_dict(record)
            rec["location"] = None
            return rec

        rec = super().station_record_to_dict(record)

        # Corfe Mullen Village Hall
        if record.polling_place_id in ["34405", "34401"]:
            rec["location"] = Point(-2.017478, 50.774375, srid=4326)
            rec["postcode"] = "BH21 3UA"

        # Portesham Village Hall
        # user issue report #38
        if record.polling_place_id == "35170":
            rec["location"] = Point(-2.567644, 50.668385, srid=4326)

        # Bishops Caundle Village Hall
        # user issue report #40
        if record.polling_place_id == "35252":
            rec["location"] = Point(-2.437757, 50.915554, srid=4326)

        # All Saints Church Hall
        # user issue report #41
        if record.polling_place_id in ["34319", "34315"]:
            rec["location"] = Point(-1.834570, 50.831005, srid=4326)

        # Ferndown Village Hall
        # user issue report #42
        if record.polling_place_id in ["34287", "34277"]:
            rec["location"] = Point(-1.896419, 50.801961, srid=4326)

        # St Marys Church Hall
        if record.polling_place_id == "35117":
            rec["location"] = Point(-2.443608, 50.709373, srid=4326)

        # Southill Community Centre
        # user issue report #47
        if record.polling_place_id == "34801":
            rec["location"] = Point(-2.477398, 50.623534, srid=4326)

        # Moose Lodge
        # user issue report #43
        if record.polling_place_id == "34771":
            rec["location"] = Point(-2.466883, 50.606307, srid=4326)

        # Charlton Marshall Parish Centre
        if record.polling_place_id == "34446":
            rec["location"] = Point(-2.14121, 50.83429, srid=4326)

        # West Moors Memorial Hall
        # user issue report #132
        if record.polling_place_id in ["34298", "34301"]:
            rec["location"] = Point(-1.89013, 50.82904, srid=4326)

        # Dorset Fire & Rescue, Peverell Avenue West...
        if record.polling_place_id == "35112":
            rec["location"] = Point(-2.471750, 50.713013, srid=4326)

        # Furzebrook Village Hall
        if record.polling_place_id == "34895":
            rec["location"] = Point(-2.10060, 50.65811, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() == "DT4 OTU":
            rec["postcode"] = "DT4 0TU"

        if record.addressline6 == "DT9 4FG":
            return None

        if record.addressline6.strip() in [
            "DT8 3DS",
            "BH20 5AL",
            "BH16 6AE",
            "DT10 1JQ",
            "DT11 7AR",
            "BH20 5ED",
        ]:
            return None

        if uprn in ["10013731265", "10013731266"]:
            rec["postcode"] = "BH20 4HA"
            rec["accept_suggestion"] = False

        if uprn in [
            "10002640153",  # DT28HW -> DT28NJ : Seafield, Holworth, Dorchester, Dorset
            "200004827271",  # BH214AD -> BH214AB : South Oak, Dullar Farm, Dullar Farm Lane, Sturminster Marshall
            "200004827507",  # BH166BA -> BH166BB : 13 Race Farm Cottages, Huntick Road, Lytchett Minster
            "10023250759",  # DT65JR -> DT65JT : The Dairy House Vearse Farm, West Road, Bridport, Dorset
            "10023250758",  # DT65JR -> DT65JT : Vearse Farmhouse, West Road, Bridport, Dorset
            "10011953652",  # BH191LT -> BH191LS : Flat 1 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953653",  # BH191LT -> BH191LS : Flat 2 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953654",  # BH191LT -> BH191LS : Flat 3 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953655",  # BH191LT -> BH191LS : Flat 4 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953656",  # BH191LT -> BH191LS : Flat 5 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953657",  # BH191LT -> BH191LS : Penthouse 1 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953658",  # BH191LT -> BH191LS : Penthouse 2 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "10011953659",  # BH191LT -> BH191LS : Penthouse 3 Spinnakers, 24 Burlington Road, Swanage, Dorset
            "100040657448",  # DT40LY -> DT40JY : Flat 2, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657451",  # DT40LY -> DT40JY : Flat 5, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657452",  # DT40LY -> DT40JY : Flat 6, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657453",  # DT40LY -> DT40JY : Flat 7, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657450",  # DT40LY -> DT40JY : Flat 4, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "100040657449",  # DT40LY -> DT40JY : Flat 3, Adelaide Court, Abbotsbury Road, Weymouth, Dorset
            "200000766574",  # DT83HY -> DT83HX : Wayland Farm, Chedington, Beaminster, Dorset
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200000767829",  # DT65BJ -> DT65BL : Caretaker`s Flat Boldwood House, 13 West Allington, Bridport, Dorset
            "100040700541",  # BH217JX -> BH217JT : High Trees Burts Lane, Mannington, Horton Heath, Wimborne, Dorset
        ]:
            rec["accept_suggestion"] = False

        return rec
