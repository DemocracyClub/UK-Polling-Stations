from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000110"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019maid.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019maid.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10091196977":
            rec["postcode"] = "TN12 9AY"

        if uprn in [
            "10091196329",  # ME144NE -> ME144NB : Annexe, 147B Ashford Road, Bearsted, Maidstone, Kent
            "200003724338",  # ME186DB -> ME186DD : Lane End, Lees Road, Laddingford, Maidstone, Kent
            "200003724339",  # ME186DY -> ME186BY : 1 Laurel Villas, Lees Road, Laddingford, Maidstone, Kent
            "200003665956",  # ME156QJ -> ME156QS : Tovil Club, Tovil Hill, Maidstone, Kent
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
            "200003729248",  # ME144AA -> ME145BH : 2 Park Villas, Ashford Road, Weavering, Maidstone, Kent
            "200003729249",  # ME144AA -> ME145BH : 4 Park Villas, Ashford Road, Weavering, Maidstone, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
