from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000119"
    addresses_name = "2020-02-10T11:11:39.774936/Democracy_Club__07May2020 Fylde.CSV"
    stations_name = "2020-02-10T11:11:39.774936/Democracy_Club__07May2020 Fylde.CSV"
    elections = ["2020-05-07"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline1 == "8 Larbreck Gardens":
            rec["postcode"] = "PR30XS"

        if record.addressline6 in [
            "PR3 0ZD",
            "PR4 0HA",
            "FY8 2PB",
            "PR4 3WD",
            "FY8 1TE",
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10023482664",  # 23 Austin Way, Carr Bridge Park, Preston New Road, Westby with Plumptons
            "10023482645",  # 5 Austin Way, Carr Bridge Park, Preston New Road, Westby with Plumptons
            "100010407320",
            "100010399482",  # 49 Church Road, St Annes
            "10013594617",  # Flat 4, 342 Clifton Drive North, Lytham St Annes
        ]:
            return None

        if uprn in [
            "10013594716",  # Old Die Cast Works
            "10013594717",  # Old Die Cast Works
            "100010410579",  # FY81YA -> FY81YB : 167 St Andrews Road South, Lytham St Annes
            "100010411187",  # FY81SB -> FY82AD : 45A St Georges Lane, Lytham St Annes
            "100010407320",  # FY82EA -> FY84EG : 10 Oxford Road, St Annes
            "100010397732",  # FY84NL -> FY84LF : 101 Bramley, Ballam Road, Lytham St Annes
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
            "10013591393",  # PR43AR -> PR41PR : 1 Rawstorne Close, Freckleton
            "10013594517",  # PR43DJ -> PR43PJ : Chestnut Lodge, Westby Road, Westby, Preston
            "10013592148",  # FY81AX -> FY85RG : Flat 13 Seville Court, Clifton Drive, Lytham St Annes
            "100010400411",  # FY85EB -> FY85ER : 33C Clifton Street, Lytham St Annes
            "100010407490",  # FY81PW -> FY81PN : 78 Park Road, Lytham St Annes
            "100010399481",  # FY85LN -> FY83TL : 45 Church Road, St Annes
            "100010409917",  # FY81NW -> FY81NP : 117 South Promenade, Lytham St Annes
            "100010407456",  # FY81PN -> FY81PW : 51 Park Road, Lytham St Annes
            "100012387934",  # FY81HY -> FY81HN : 291 Clifton Drive South, Lytham St Annes
            "200001782201",  # FY81NW -> FY81WB : 10 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100010407474",  # FY81PN -> FY81PW : 65 Park Road, Lytham St Annes
            "100010409914",  # FY81NW -> FY81LS : St Ives Hotel, 7- 9 South Promenade, Lytham St Annes
            "100012389320",  # FY81NW -> FY81WA : 3 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100012618349",  # FY81NW -> FY81WB : 3 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100012389324",  # FY81NW -> FY81WA : 7 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100012618353",  # FY81NW -> FY81WB : 7 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100010412796",  # FY85DG -> FY85DX : First Floor Flat, 2A East Cliffe, Lytham St Annes
            "100012388934",  # FY82QX -> FY83QX : Mabie, Otley Road, Lytham St Annes
            "100012388296",  # FY81TP -> FY81SP : Flat 2 Newfield Court, Hove Road, Lytham St Annes
            "100012389326",  # FY81NW -> FY81WA : 9 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100012389327",  # FY81NW -> FY81WA : 10 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100010401714",  # FY85EU -> FY85EX : 20 East Beach, Lytham St Annes
            "100012388299",  # FY81TP -> FY81SP : Flat 5 Newfield Court, Hove Road, Lytham St Annes
            "100012388298",  # FY81TP -> FY81SP : Flat 4 Newfield Court, Hove Road, Lytham St Annes
            "100012388300",  # FY81TP -> FY81SP : Flat 6 Newfield Court, Hove Road, Lytham St Annes
            "100012618347",  # FY81NW -> FY81WB : 1 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100012389323",  # FY81NW -> FY81WA : 6 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100012618352",  # FY81NW -> FY81WB : 6 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100010405063",  # FY83BF -> FY83BN : 140 Kilnhouse Lane, Lytham St Annes
            "100012388297",  # FY81TP -> FY81SP : Flat 3 Newfield Court, Hove Road, Lytham St Annes
            "10013594718",  # FY85DG -> FY85DX : Ground Floor Flat, 2B East Cliffe, Lytham St Annes
            "100012389319",  # FY81NW -> FY81WA : 1 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100012618350",  # FY81NW -> FY81WB : 4 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100012388220",  # FY83RW -> FY83RT : 20 Heyhouses Lane, Lytham St Annes, Lancs
            "100010397734",  # FY84NL -> FY84LF : 105 Ballam Road, Lytham St Annes
            "100010397735",  # FY84NL -> FY84LF : Lowood, 109 Ballam Road, Lytham St Annes
            "100010397736",  # FY84NL -> FY84LF : Carency, 111 Ballam Road, Lytham St Annes
            "100012387585",  # FY84NG -> FY84NP : Watchwood House, Watchwood Drive, Lytham St Annes
            "100010397737",  # FY84NL -> FY84LF : Barn Gate 113, Ballam Road, Lytham St Annes
            "100012388284",  # FY83RS -> FY83RG : Flat 6 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100012388285",  # FY83RS -> FY83RG : Flat 7 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100012388283",  # FY83RS -> FY83RG : Flat 5 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100012388282",  # FY83RS -> FY83RG : Flat 4 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "10013591110",  # FY84PS -> FY84FS : 3 Monks Gate, Lytham St Annes
            "10013591111",  # FY84PS -> FY84FS : 5 Monks Gate, Lytham St Annes
            "100010412504",  # FY81LE -> FY85DZ : 21A Victoria Street, Lytham St Annes
            "100010401738",  # FY85EX -> FY85EY : 41A East Beach, Lytham St Annes
            "100010397649",  # FY84BU -> FY84BS : 16 Badgers Walk East, Lytham St Annes
            "100012388287",  # FY83RS -> FY83RG : Flat 9 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100010397650",  # FY84BU -> FY84BS : 17 Badgers Walk East, Lytham St Annes
            "100010400141",  # FY82QZ -> FY82QX : 515A Clifton Drive North, Lytham St Annes
            "100010401741",  # FY85EX -> FY85EY : 43A East Beach, Lytham St Annes
            "100010401739",  # FY85EX -> FY85EY : 41 East Beach, Lytham St Annes
            "100012388167",  # FY85DY -> FY85DS : 7 Freckleton Court, Lytham St Annes
            "100010397654",  # FY84BU -> FY84BS : 21 Badgers Walk East, Lytham St Annes
            "100010397657",  # FY84BU -> FY84BS : 24 Badgers Walk East, Lytham St Annes
            "100012388166",  # FY85DY -> FY85DS : 6 Freckleton Court, Lytham St Annes
            "100010397655",  # FY84BU -> FY84BS : 22 Badgers Walk East, Lytham St Annes
            "100010397656",  # FY84BU -> FY84BS : 23 Badgers Walk East, Lytham St Annes
            "100010403100",  # FY82LY -> FY83LY : 2 Greenways, Lytham St Annes
            "100010397658",  # FY84BU -> FY84BS : 25 Badgers Walk East, Lytham St Annes
            "10013591112",  # FY84PS -> FY84FS : 2 Monks Gate, Lytham St Annes
            "100010397663",  # FY84BU -> FY84BS : 30 Badgers Walk East, Lytham St Annes
            "100010397662",  # FY84BU -> FY84BS : 29 Badgers Walk East, Lytham St Annes
            "100010397651",  # FY84BU -> FY84BS : 18 Badgers Walk East, Lytham St Annes
            "10091660123",  # FY81TB -> FY81TF : Flat 1, 15 St Davids Road South, Lytham St Annes
            "10091660125",  # FY81TB -> FY81TF : Flat 3, 15 St Davids Road South, Lytham St Annes
            "100012388161",  # FY85DY -> FY85DS : 1 Freckleton Court, Lytham St Annes
            "100010397664",  # FY84BU -> FY84BS : 31 Badgers Walk East, Lytham St Annes
            "100012389322",  # FY81NW -> FY81WA : 5 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100010397660",  # FY84BU -> FY84BS : 27 Badgers Walk East, Lytham St Annes
            "100012618354",  # FY81NW -> FY81WB : 8 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100012388162",  # FY82DY -> FY85DS : 2 Freckleton Court, Lytham St Annes
            "100012388164",  # FY85DY -> FY85DS : 4 Freckleton Court, Lytham St Annes
            "100012388280",  # FY83RS -> FY83RG : Flat 2 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100012388286",  # FY83RS -> FY83RG : Flat 8 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100012388281",  # FY83RS -> FY83RG : Flat 3 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100010401742",  # FY85EX -> FY85EY : 43 East Beach, Lytham St Annes
            "10013591113",  # FY84PS -> FY84FS : 4 Monks Gate, Lytham St Annes
            "100012618348",  # FY81NW -> FY81WB : 2 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100012389321",  # FY81NW -> FY81WA : 4 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100012389325",  # FY81NW -> FY81WA : 8 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "10091660124",  # FY81TB -> FY81TF : Flat 2, 15 St Davids Road South, Lytham St Annes
            "100012388163",  # FY85DY -> FY85DS : 3 Freckleton Court, Lytham St Annes
            "100012618394",  # FY81NW -> FY81WB : 9 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100010397738",  # FY84NL -> FY84LF : Woodside, 117 Ballam Road, Lytham St Annes
            "10013591109",  # FY84PS -> FY84FS : 1 Monks Gate, Lytham St Annes
            "100012388295",  # FY81TP -> FY81SP : Flat 1 Newfield Court, Hove Road, Lytham St Annes
            "100010408199",  # FY81PW -> FY83UZ : 3 Richards Way, Lytham St Annes
            "100010397666",  # FY84BU -> FY84BS : 33 Badgers Walk East, Lytham St Annes
            "100012618351",  # FY81NW -> FY81WB : 5 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100010401715",  # FY85EU -> FY85EX : The Cottage, 21A East Beach, Lytham St Annes
            "100010397667",  # FY84BU -> FY84BS : 34 Badgers Walk East, Lytham St Annes
            "10013592171",  # FY81NN -> FY81PD : Amelia, Fairhaven Lane, Lytham St Annes
            "100012388168",  # FY85DY -> FY85DS : 8 Freckleton Court, Lytham St Annes
            "100012389328",  # FY81NW -> FY81WA : 11 Vernon Lodge, 99 South Promenade, Lytham St Annes
            "100010397653",  # FY84BU -> FY84BS : 20 Badgers Walk East, Lytham St Annes
            "100010397665",  # FY84BU -> FY84BS : 32 Badgers Walk East, Lytham St Annes
            "100010397652",  # FY84BU -> FY84BS : 19 Badgers Walk East, Lytham St Annes
            "100012388165",  # FY85DY -> FY85DS : 5 Freckleton Court, Lytham St Annes
            "100010397648",  # FY84BU -> FY84BS : 15 Badgers Walk East, Lytham St Annes
            "100012388279",  # FY83RS -> FY83RG : Flat 1 Willow Lodge, 226 Heyhouses Lane, Lytham St Annes
            "100012618395",  # FY81NW -> FY81WB : 11 Hillcliffe, 95 South Promenade, Lytham St Annes
            "100010397733",  # FY84NL -> FY84LF : 103 Ballam Road, Lytham St Annes
            "100010397661",  # FY84BU -> FY84BS : 28 Badgers Walk East, Lytham St Annes
            "100010407437",  # FY81PN -> FY81PW : 39 Park Road, Lytham St Annes
            "100010397659",  # FY84BU -> FY84BS : 26 Badgers Walk East, Lytham St Annes
            "100012389995",  # FY84DZ -> FY84EP : Flat 1 The Blossoms Hotel, Woodlands Road, Lytham St Annes
            "100012389991",  # FY84DZ -> FY84EP : Flat 2 The Blossoms Hotel, Woodlands Road, Lytham St Annes
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100012754283",  # PR42BH -> PR42BD : Grammar School, Ribby Road, Kirkham
            "100010421084",  # PR42HA -> PR43AD : 48 Station Road, Kirkham
            "100010399485",  # FY83NE -> FY85LH : 6 Church Road, St Annes
            "100010417936",  # PR41AA -> PR41AD : 21 Lytham Road, Freckleton
            "100010417965",  # PR41AB -> PR41AD : 67 Lytham Road, Freckleton
            "100012753622",  # PR41AD -> PR41AB : 79 Lytham Road, Bryning-with-Warton
            "100010421067",  # PR42AS -> PR43AD : 20 Station Road, Kirkham
            "100010421087",  # PR42HD -> PR43AA : 51- 53 Station Road, Kirkham
            "100010421129",  # PR43AA -> PR42AS : 21 Station Road, Medlar-with-Wesham
            "100010421150",  # PR43AA -> PR42HD : 69 Station Road, Medlar-with-Wesham
            "100012388053",  # FY85EY -> FY85EX : Maisonette, 42 East Beach, Lytham St Annes
        ]:
            rec["accept_suggestion"] = False

        return rec
