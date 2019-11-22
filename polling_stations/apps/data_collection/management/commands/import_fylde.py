from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000119"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019fylde.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019fylde.CSV"
    elections = ["parl.2019-12-12"]
    match_threshold = 96
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["PR3 0ZD", "PR4 0HA"]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100012620038",
            "100010407320",
            "100010418002",
            "100010399482",
            "10013594617",
        ]:
            # Misplaced properties
            return None

        if uprn == "100012391142":
            rec["postcode"] = "PR4 0RN"

        if uprn == "200001128516":
            rec["postcode"] = "FY6 9BU"

        if record.addressline2 == "Plumpton Lane" and record.addressline6 == "PR4 3WD":
            rec["accept_suggestion"] = True

        if uprn in [
            "100010410579",  # FY81YA -> FY81YB : 167 St Andrews Road South, Lytham St Annes
            "100010411172",  # FY81TS -> FY81TY : 55 St Davids Road South, Lytham St Annes
            "100012619511",  # FY82JT -> FY82JS : 191 St Davids Road North, Lytham St Annes
            "100010411187",  # FY81SB -> FY82AD : 45A St Georges Lane, Lytham St Annes
            "100010407300",  # FY84EG -> FY82EA : 3 Oxford Road, St Annes
            "100010407314",  # FY84EG -> FY82EA : 16 Oxford Road, St Annes
            "100010407316",  # FY84EG -> FY82EA : 18 Oxford Road, St Annes
            "100010407320",  # FY82EA -> FY84EG : 10 Oxford Road, St Annes
            "100010407312",  # FY84EG -> FY82EA : 14 Oxford Road, St Annes
            "10023483661",  # FY81HY -> FY81NH : Flat 2, 230 Clifton Drive South, Lytham St Annes
            "100010397732",  # FY84NL -> FY84LF : 101 Bramley, Ballam Road, Lytham St Annes
            "100010411162",  # FY81TS -> FY81TJ : Rear Ground Floor, 46 St Davids Road South, Lytham St Annes
            "10013592394",  # FY45EB -> FY45EA : Brookvale, Division Lane, Marton Moss, Blackpool
            "10013591504",  # PR43WD -> PR43NE : Manderley, Singleton Road, Great Plumpton, Preston
            "100012620293",  # FY84NL -> FY84NJ : Cedar Lodge, Ballam Road, Ballam, Lytham St.Annes
            "100012387556",  # FY84NJ -> FY84NH : Ballam Lodge, Ballam Road, Ballam, Lytham St.Annes
            "10023481138",  # FY84LE -> FY84NG : Lawns Farm, Ballam Road, Ballam, Lytham St.Annes
            "10013591723",  # FY81PQ -> PR42PJ : Fox Lane Ends Cottage, Fox Lane Ends, Wrea Green, Preston
            "100012392019",  # PR42NA -> PR43NA : Alanice View, Weeton Road, Medlar-with-Wesham
            "100010414855",  # PR42JW -> PR42WJ : 38 Bryning Lane, Ribby-with-Wrea
            "100010420266",  # PR42JN -> PR42NJ : 24 Richmond Avenue, Ribby-with-Wrea
            "100012387587",  # FY84NG -> FY84NQ : White Lodge, Ballam Road, Ballam, Lytham St.Annes
            "100012392002",  # PR43RX -> PR43RY : Coronation Villa, Moor Hall Lane, Newton-with-Clifton
            "100012392007",  # PR43RX -> PR43RY : Willow Dene, Moor Hall Lane, Newton-with-Clifton
            "100012390526",  # PR43RL -> PR43RN : Bryndette, Bryning Lane, Newton-with-Clifton
            "100012390537",  # PR43RN -> PR43RL : Glenrowan, Bryning Lane, Newton-with-Clifton
            "100012390535",  # PR43RL -> PR43RN : Glenforsa, Bryning Lane, Newton-with-Clifton
            "100012390521",  # PR43RN -> PR43RL : Alderley, Bryning Lane, Newton-with-Clifton
            "100012390523",  # PR43RN -> PR43RL : Beech House, Bryning Lane, Newton-with-Clifton
            "100012753544",  # PR40XL -> PR40XD : Merville Bungalow, Blackpool Road, Newton-with-Clifton
            "100012390298",  # PR43HS -> PR43HN : Stanley Villa Farm, Back Lane, Weeton
            "100012620275",  # FY84FT -> FY84JE : Flat 6 Arcon House 6-12, Park View Road, Lytham St Annes
            "10013591393",  # PR43AR -> PR41PR : 1 Rawstorne Close, Freckleton
            "10013594517",  # PR43DJ -> PR43PJ : Chestnut Lodge, Westby Road, Westby, Preston
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100012754283",  # PR42BH -> PR42BD : Grammar School, Ribby Road, Kirkham
            "100010421084",  # PR42HA -> PR43AD : 48 Station Road, Kirkham
            "100010421116",  # PR42AS -> PR43DQ : 8 Station Road, Kirkham
            "10023481541",  # FY85PR -> FY85RD : Lynfield, 49 Church Road, Lytham
            "100010399485",  # FY83NE -> FY85LH : 6 Church Road, St Annes
            "100010417936",  # PR41AA -> PR41AD : 21 Lytham Road, Freckleton
            "100010417965",  # PR41AB -> PR41AD : 67 Lytham Road, Freckleton
            "100012753661",  # PR41XD -> PR41XA : 16 Lytham Road, Bryning-with-Warton
            "100012834588",  # PR41AD -> PR41AA : 19 Lytham Road, Bryning-with-Warton
            "100010418049",  # PR41AD -> PR41AA : 21 Lytham Road, Bryning-with-Warton
            "100012753872",  # PR41XD -> PR41XA : 64 Lytham Road, Bryning-with-Warton
            "100012753622",  # PR41AD -> PR41AB : 79 Lytham Road, Bryning-with-Warton
            "10013591600",  # PR42AS -> PR43AA : 10 Station Road, Kirkham
            "100010421067",  # PR42AS -> PR43AD : 20 Station Road, Kirkham
            "100010421087",  # PR42HD -> PR43AA : 51- 53 Station Road, Kirkham
            "100012753973",  # PR43AD -> PR42AS : 14 Station Road, Medlar-with-Wesham
            "100010421129",  # PR43AA -> PR42AS : 21 Station Road, Medlar-with-Wesham
            "100012753975",  # PR43AD -> PR42AS : 26 Station Road, Medlar-with-Wesham
            "100010421150",  # PR43AA -> PR42HD : 69 Station Road, Medlar-with-Wesham
            "10023483086",  # FY81RF -> FY81SB : Flat 1 Back 42, St Annes Road West, Lytham St Annes
            "10023483087",  # FY81RF -> FY81SB : Flat 2 Back 42, St Annes Road West, Lytham St Annes
            "10023483088",  # FY81RF -> FY81SB : Flat 3 Back 42, St Annes Road West, Lytham St Annes
            "100012388053",  # FY85EY -> FY85EX : Maisonette, 42 East Beach, Lytham St Annes
        ]:
            rec["accept_suggestion"] = False

        return rec
