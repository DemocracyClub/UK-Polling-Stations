from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000005"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019 Chesham & Amersham.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019 Chesham & Amersham.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "HP5 SPJ":
            record = record._replace(addressline6="HP5 2PJ")

        if record.addressline6 in ["HP16 0HR", "HP5 1JY"]:
            return None  # surprising polling station assignments

        if uprn == "10013777238":
            record = record._replace(addressline6="HP16 0RL")

        rec = super().address_record_to_dict(record)

        if uprn in [
            # both postcodes look wrong
            "10003904383",  # Misbourne Suite, Rayners Extra Care Home, Weedon Hill, Hyde Heath, Amersham, Bucks
        ]:
            return None

        if uprn in [
            "100081184958",  # HP52HF -> HP52HG : 115 Bellingdon Road, Chesham, Bucks
            "200003031219",  # HP65RP -> HP65RW : Redlands, The Green, Hyde Heath, Amersham, Bucks
            "200003031221",  # HP65RP -> HP65RW : Troy Cottage, The Green, Hyde Heath, Amersham, Bucks
            "100081186932",  # HP79AZ -> HP79RZ : 268 Chiltern Heights, White Lion Road, Little Chalfont, Amersham
            "100081077865",  # HP66PG -> HP66PQ : Beech Hanger, 112 Bell Lane, Little Chalfont, Amersham, Bucks
            "10013780932",  # SL99FH -> SL90FH : 3 Drury Close, Chalfont Dene, Chalfont St Peter, Bucks
            "100081082308",  # HP51TW -> HP51TP : Willow Cottage, Latimer Road, Chesham, Bucks
            "10013781205",  # SL99LS -> SL99LX : Overdale Cottage, Nicol Road, Chalfont St Peter, Bucks
            "100081083675",  # SL98RP -> SL98RS : Woolton House, Maltmans Lane, Chalfont St Peter, Gerrards Cross
            "100081280755",  # SL98RS -> SL98RP : The Old Malt House, Maltmans Lane, Chalfont St Peter, Gerrards Cross
            "100081187111",  # HP84BP -> HP84BW : Pine Acre, Burtons Way, Chalfont St Giles
            "200003036501",  # HP169LQ -> HP160RR : Ballinger Meadow, Herberts Hole, Great Missenden
            "10012939600",  # HP169BY -> HP169BG : St Martins, Grimms Hill, Great Missenden, Bucks
            "100080498318",  # HP66RT -> HP66SE : The Grove, 19 Amersham Road, Little Chalfont
            "100081080415",  # HP84EE -> HP84EF : Bow Wood Barn, Bottom House Lane, Chalfont St. Giles, Bucks
            "200003030834",  # HP160LR -> HP160RL : Hawthorn Farm, Hyde End, Chesham Road, Great Missenden, Bucks
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10013777238",  # see postcode fix for this UPRN above
        ]:
            rec["accept_suggestion"] = False

        return rec
