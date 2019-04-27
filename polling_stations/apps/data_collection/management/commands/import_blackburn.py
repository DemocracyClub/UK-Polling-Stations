from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000008"
    addresses_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019BwD.tsv"
    stations_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019BwD.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

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
            "10010320288",  # BB11SP -> BB11RF : 54 Nottingham Street, Blackburn
            "10010322769",  # BB15AT -> BB24QR : White Bull Flat, 62 Church Street, Blackburn
            "200004500538",  # BB12ND -> BB30HN : 203 Haslingden Road, Blackburn
            "10010324291",  # BB31EJ -> BB21AD : Flat at, 47A Blackburn Road, Darwen
            "10010324284",  # BB31AR -> BB21AD : Flat over, 29 Duckworth Street, Darwen
            "10010324283",  # BB33HS -> BB21AD : Flat at, 15 Entwistle Street, Darwen
            "10010324288",  # BB14AA -> BB21AD : Cunliffe Farm, 1 Whalley Old Road, Blackburn
            "10010324282",  # BB15NR -> BB21AD : Flat At, 3 Rydal Road, Blackburn
            "10010324293",  # BB15PW -> BB21AD : Flat Over, 46 Warrington Street, Blackburn
            "10010324286",  # BB15PQ -> BB21AD : Flat Above, 171 Whalley Old Road, Blackburn
            "10010324289",  # BB15PQ -> BB21AD : Flat At, 195 Whalley Old Road, Blackburn
            "10010324287",  # BB15PD -> BB21AD : Flat Over, 260 Whalley Old Road, Blackburn
            "10010324290",  # BB12AL -> BB21AD : Flat Over, 267/269 Accrington Road, Blackburn
            "10010324285",  # BB13JY -> BB21AD : 33 Brecon Road, Blackburn
            "100010774379",  # BB25NT -> BB32DS : 18 Sunnyside Avenue, Cherry Tree, Blackburn
            "10010324961",  # BB19PE -> BB18QJ : 91 Warrenside Close, Blackburn
            "10024629613",  # BB26NP -> BB26NB : Claremont, 54 Saunders Road, Blackburn
            "100010741593",  # BB26JS -> BB26JW : 39 Granville Road, Blackburn
            "200004510512",  # BB33QQ -> BL70BB : Manor Cottage 4 Scholes Fold, Pickup Bank, Darwen
            "200004504520",  # BB32DL -> BB13AZ : 3 Edmund Street, Darwen
            "10010322864",  # BB24JX -> BB32DL : Flat Over, 2 Edmund Street, Blackburn
            "10010322864",  # BB24JX -> BB32DL : 2 Edmund Street, Blackburn
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
            "10024630099",  # BB11RF -> BB11RG : 42 Queen`s Park Road, Blackburn
            "10010322856",  # BB22NS -> BB33DB : Flat over, 42 Sandon Street, Blackburn
            "10024627903",  # BB24JQ -> BB32PS : 378A Bolton Road, Blackburn
            "10010322654",  # BB24LU -> BB24RA : Flat At Brown Cow Inn, 125 Livesey Branch Road, Blackburn
            "200004501432",  # BB15BY -> BB15BX : Bank Cottage, Eanam, Blackburn
            "100012425258",  # BB26NG -> BB26NH : Viewfield Mews, 6 Oozehead Lane, Blackburn
        ]:
            rec["accept_suggestion"] = False

        return rec
