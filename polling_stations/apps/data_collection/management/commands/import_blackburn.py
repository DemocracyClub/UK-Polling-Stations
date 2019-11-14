from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000008"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "3685":
            record = record._replace(polling_place_postcode="BB2 2JR")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10010322805":
            rec["postcode"] = "BB1 7JN"

        if uprn == "10024626643":
            rec["postcode"] = "BL7 0HL"

        if record.addressline6.strip() == "BB2 2AX":
            return None

        if uprn in [
            "100010760451",  # BB18ET -> BB18HH : 146 St. James`s Road, Blackburn
            "100012426844",  # BB30LG -> BB30LR : Holden Fold, Tockholes Road, Darwen
            "200004506573",  # BB31JY -> BB31LJ : Higher Woodhead Farm, Off Willow Bank Lane, Darwen
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10010324293",  # BB15PW -> BB21AD : Flat Over, 46 Warrington Street, Blackburn
            "10010324286",  # BB15PQ -> BB21AD : Flat Above, 171 Whalley Old Road, Blackburn
            "10010324289",  # BB15PQ -> BB21AD : Flat At, 195 Whalley Old Road, Blackburn
            "10010324285",  # BB13JY -> BB21AD : 33 Brecon Road, Blackburn
            "10010324961",  # BB19PE -> BB18QJ : 91 Warrenside Close, Blackburn
            "10024629613",  # BB26NP -> BB26NB : Claremont, 54 Saunders Road, Blackburn
            "100010741593",  # BB26JS -> BB26JW : 39 Granville Road, Blackburn
            "100012426752",  # BB33PJ -> BB33BN : Belaire, Roman Road, Eccleshill, Darwen
            "100012426754",  # BB33PJ -> BB33BN : Glenmere, Roman Road, Eccleshill, Darwen
            "100012426743",  # BB33PJ -> BB33BN : Landwyn, Roman Road, Eccleshill, Darwen
            "100012426751",  # BB33PJ -> BB33BN : Ainsdale, Roman Road, Eccleshill, Darwen
            "100012426757",  # BB33PJ -> BB33BN : Melrose, Roman Road, Eccleshill, Darwen
            "100012426758",  # BB33PJ -> BB33BN : Ravensgarth, Roman Road, Eccleshill, Darwen
            "100012542507",  # BB33PJ -> BB33BN : Windyridge, 25 Roman Road, Eccleshill, Darwen
            "100012426761",  # BB33PJ -> BB33BN : Thornville, Roman Road, Eccleshill, Darwen
            "10010322588",  # BB12AE -> BB12AH : Flat At, 158 Accrington Road, Blackburn
            "10024630259",  # BB26BT -> BB26JB : Flat at, 3 Limefield, Blackburn
            "10010322856",  # BB22NS -> BB33DB : Flat over, 42 Sandon Street, Blackburn
            "10024627903",  # BB24JQ -> BB32PS : 378A Bolton Road, Blackburn
            "10010322654",  # BB24LU -> BB24RA : Flat At Brown Cow Inn, 125 Livesey Branch Road, Blackburn
            "100012425258",  # BB26NG -> BB26NH : Viewfield Mews, 6 Oozehead Lane, Blackburn
        ]:
            rec["accept_suggestion"] = False

        return rec
