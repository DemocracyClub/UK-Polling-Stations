from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000110"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019maid.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019maid.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "1888":
            record = record._replace(polling_place_postcode="ME15 6RE")
        if record.polling_place_id == "1852":
            record = record._replace(polling_place_postcode="ME9 0TT")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.post_code == "ME17 4FT":
            return None

        if uprn == "10091196977":
            rec["postcode"] = "TN12 9AY"

        if uprn in ["200003728216"]:
            return None

        if uprn in [
            "10091196329",  # ME144NE -> ME144NB : Annexe, 147B Ashford Road, Bearsted, Maidstone, Kent
            "200003724338",  # ME186DB -> ME186DD : Lane End, Lees Road, Laddingford, Maidstone, Kent
            "200003724339",  # ME186DY -> ME186BY : 1 Laurel Villas, Lees Road, Laddingford, Maidstone, Kent
            "200003665956",  # ME156QJ -> ME156QS : Tovil Club, Tovil Hill, Maidstone, Kent
            "200003724788",  # ME173EX -> ME174DA : Horseshoes Paddock, Lucks Lane, Boughton Monchelsea, Maidstone, Kent
            "10022901403",  # ME160EE -> ME160EG : Sunli, 2 Giddyhorn Lane, Maidstone, Kent
            "200003721478",  # ME173HZ -> ME173JB : Highlands, Chartway Street, East Sutton, Maidstone, Kent
            "200003728036",  # ME171LG -> ME171LP : Wheelwrights, Windmill Hill, Ulcombe, Maidstone, Kent
            "200003722515",  # ME171XJ -> ME171XH : The Firs, Firs Lane, Hollingbourne, Maidstone, Kent
            "200003701917",  # ME97RY -> ME97RZ : South Leas Farm, South Lees, South Green, Sittingbourne, Kent
            "200003729424",  # ME159RA -> ME158RA : Tollgate, Sutton Road, Maidstone, Kent
            "200003654941",  # TN120RL -> TN120RW : Fleet Farm, Maidstone Road, Staplehurst, Tonbridge, Kent
            "200003732255",  # ME173SW -> ME173SP : Mount Pleasant Farm Oast, Brishing Road, Langley, Maidstone, Kent
            "200003729248",  # ME144AA -> ME145BH : 2 Park Villas, Ashford Road, Weavering, Maidstone, Kent
            "200003729249",  # ME144AA -> ME145BH : 4 Park Villas, Ashford Road, Weavering, Maidstone, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10091193486",  # ME143EP -> ME143AS : Oak Spring Lake, Sittingbourne Road, Detling, Maidstone, Kent
            "200003731903",  # ME171BL -> ME171HX : The Roebuck Inn, Ashford Road, Harrietsham, Maidstone, Kent
            "200003714599",  # ME172BT -> ME172DS : New Shelve Farm, Forstal Road, Lenham, Maidstone, Kent
            "200003731686",  # ME173JB -> ME173NR : 3 Bridgefield, Chartway Street, Kingswood, Maidstone, Kent
            "200003731687",  # ME173JB -> ME173NR : 4 Bridgefield, Chartway Street, Kingswood, Maidstone, Kent
            "200003728938",  # ME142BH -> ME168DP : Second Floor Flat 3, 229 Boxley Road, Maidstone, Kent
            "10014306125",  # ME156EU -> ME168HB : Studio 1, 29A Upper Stone Street, Maidstone, Kent
            "200003661581",  # ME186EF -> ME150QR : 1 Buston Manor Farm Cottages, Lughorse Lane, Yalding, Maidstone, Kent
            "10014306926",  # ME157AH -> ME158BF : Parkside, 8 South Park Road, Maidstone, Kent
            "10014307985",  # ME160UR -> ME172JB : The Old Fruit Store, 17 Tarragon Road, Maidstone, Kent
            "200003656987",  # ME90DH -> ME185HD : Green Farm, Wichling, Sittingbourne, Kent
            "200003734477",  # ME173AW -> ME156LL : The Court House, Chart Road, Sutton Valence, Maidstone, Kent
            "200003711186",
        ]:
            rec["accept_suggestion"] = False

        return rec
