from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000046"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019torr.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019torr.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7148":
            # Buckland Filleigh Village Hall BUCKLAND FILLEIGH
            record = record._replace(polling_place_postcode="EX21 5HZ")

        if record.polling_place_id == "7274":
            # St Giles In the Wood Parish Hall St Giles In the Wood TORRINGTON
            record = record._replace(polling_place_postcode="EX38 7JH")

        if record.polling_place_id == "7078":
            # Appledore - St Mary`s Church Hall, Appledore, BIDEFORD
            record = record._replace(polling_place_postcode="EX39 1RL")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.lstrip("0")

        if record.addressline6 in (
            "EX39 6HN",
            "EX39 6EP",
            "EX39 6EN",
            "EX39 6HB",
            "EX39 5SL",
            "EX39 1HA",
            "EX39 1HB",
        ):
            # multi_address odd-looking station assignment
            return None

        if uprn in [
            "10002296905",  # EX226YB -> EX226LN : Four Acres, Derril, Pyworthy, HOLSWORTHY
            "10002299062",  # EX215HA -> EX215EJ : Clarendon House, Ashwater Hill, Ashwater, BEAWORTHY
            "10002299668",  # EX227ND -> EX227BN : Willow Spring, Beacon, HOLSWORTHY
            "10002299686",  # EX395DY -> EX395DZ : Johns Cottage, 16 Bucks Mills, BIDEFORD
            "10002300021",  # EX395NL -> EX395NN : Stonewold Bungalow, Collingsdown, Buckland Brewer, BIDEFORD
            "10002300274",  # EX388LS -> EX388LR : Ford Haven, Downmoor Cross, Newton St Petrock, TORRINGTON, Devon
            "10002301419",  # EX227DH -> EX227ND : The Hollies, Holsworthy Beacon, HOLSWORTHY
            "10002301749",  # EX387JU -> EX387LA : Cranford Inn, St Giles In the Wood, TORRINGTON
            "10003500004",  # EX395JH -> EX395JQ : Damn View, Coach Drive, BIDEFORD
            "10003502700",  # EX388AX -> EX388AY : Oakimber, Limers Hill, TORRINGTON
            "10003502703",  # EX388AX -> EX388AY : Talami, Mill Street Common, Limers Hill, TORRINGTON
            "10003502708",  # EX388AX -> EX388AY : Crakyland, Mill Street Common, Limers Hill, TORRINGTON
            "10003502709",  # EX388AX -> EX388AY : Wayfarers, Mill Street Common, Limers Hill, TORRINGTON
            "10003504562",  # EX388DN -> EX388DL : Woodland Vale, New Street, TORRINGTON
            "100040372654",  # EX391PU -> EX393PU : Culverkeys, Buckleigh Road, Westward Ho!, BIDEFORD
            "100040372673",  # EX391PU -> EX393PU : 4 Southmoor, Buckleigh Road, Westward Ho!, BIDEFORD
            "10013842863",  # EX385RA -> EX395RA : 42 Hartland Forest Golf & Leisure Parc, Woolsery, BIDEFORD
            "10091078210",  # EX227TD -> EX227DT : Annexe, Underwood Hayes, South Wonford, Thornbury, HOLSWORTHY
            "10093910069",  # EX395HN -> EX393HN : Mobile Home 1, Unit 3C Clovelly Road Industrial Estate, BIDEFORD
            "10093912196",  # EX215HN -> EX215HD : Agricultural Workers Dwelling, Thorndon House, Ashwater, Beaworthy
            "10023352605",  # EX395HQ -> EX215HQ : The Longhouse, West Road, Sheepwash, BEAWORTHY
            "10003507766",  # EX388QH -> EX388QT : The Yard, Woolaton, Woolaton, Peters Marland, TORRINGTON
            "10002297258",  # EX227HU -> EX227HX : 1 Hill View, HOLSWORTHY, Devon
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10002299987",  # EX227DQ -> EX227DE : The Jays Forge, Thornbury, HOLSWORTHY
            "10002299992",  # EX227DH -> EX227DQ : Kites, Strawberry Bank, Milton Damerel, HOLSWORTHY
            "10023351252",  # EX198HA -> EX198PP : Jubilee Park Farm, Loosedown Cross, WINKLEIGH
        ]:
            rec["accept_suggestion"] = False

        return rec
