from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000110"
    addresses_name = "parl.2019-12-12/Version 1/maidstone.gov.uk-1573749536000-.tsv"
    stations_name = "parl.2019-12-12/Version 1/maidstone.gov.uk-1573749536000-.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "2444":
            # St Stephens Day Centre 1 St Stephens Square Tovil Maidstone
            record = record._replace(polling_place_postcode="ME15 6RE")
        if record.polling_place_id == "2303":
            # Wormshill Village Hall Wormshill Sittingbourne
            record = record._replace(polling_place_postcode="ME9 0TT")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "TN12 9A7":
            rec["postcode"] = "TN12 9AY"

        if uprn == "200003729703":
            rec["postcode"] = "ME15 8HE"
            rec["accept_suggestion"] = False

        if record.addressline6 == "ME9 7RT":
            return None

        if uprn in [
            "200003724338",  # ME186DB -> ME186DD : Lane End, Lees Road, Laddingford, Maidstone, Kent
            "200003724339",  # ME186DY -> ME186BY : 1 Laurel Villas, Lees Road, Laddingford, Maidstone, Kent
            "200003665956",  # ME156QJ -> ME156QS : Tovil Club, Tovil Hill, Maidstone, Kent
            "200003724788",  # ME173EX -> ME174DA : Horseshoes Paddock, Lucks Lane, Boughton Monchelsea, Maidstone, Kent
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
            "10014306125",  # ME156EU -> ME168HB : Studio 1, 29A Upper Stone Street, Maidstone, Kent
            "200003661581",  # ME186EF -> ME150QR : 1 Buston Manor Farm Cottages, Lughorse Lane, Yalding, Maidstone, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
