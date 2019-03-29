from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000008"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.CSV"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)
        postcode = record.addressline6

        if uprn == "200002851978":
            rec["postcode"] = "M43 7RZ"
            return rec

        # Clearly wrong but too many to sort out
        if uprn in [
            "100012486537",
            "100012486572",
            "100012776038",
            "100012777167",
            "10014259385",
            "10090073761",
            "10090073763",
            "10090073764",
            "200004407864",
            "200004407867",
            "200004410055",
            "200004410061",
            "200004410550",
            "200004410656",
            "200004422675",
            "200004423681",
        ] or postcode in ["SK14 1EY", "SK14 4XE", "SK14 4EG", "M34 2WS", "OL6 7FU"]:
            return None

        if uprn in [
            "10014259345",  # SK153AE -> SK153AD : 2 Portland Chambers, 1 Mottram Road, Stalybridge, Cheshire
            "100012486293",  # SK146SE -> SK146SJ : Mains Grass Farm, Edge Lane, Mottram, Hyde, Cheshire
            "10003436096",  # SK146SQ -> SK146SG : The Cottage,Landslow Green, Hobson Moor Road, Mottram, Hyde, Cheshire
            "100011618417",  # SK151AD -> SK153AD : 6A Portland Place, Mottram Road, Stalybridge, Cheshire
            "10003434537",  # OL59PH -> OL50BA : The Penthouse, Stamford Road, Mossley, Ashton-under-Lyne, Lancashire
            "100012776537",  # SK145QG -> SK145QN : Cemetery Lodge, Stockport Road, Hyde, Cheshire
            "100011609197",  # M346AJ -> M346AF : 75A Town Lane, Denton, Manchester
            "100012487649",  # M437LN -> M437FS : Meadow View Farm, Lumb Lane, Droylsden, Manchester
            "100011536589",  # OL66NR -> OL69NR : 4 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536590",  # OL66NR -> OL69NR : 6 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536591",  # OL66NR -> OL69NR : 8 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536592",  # OL66NR -> OL69NR : 12 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536593",  # OL66NR -> OL69NR : 14 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536594",  # OL66NR -> OL69NR : 16 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536595",  # OL66NR -> OL69NR : 18 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536596",  # OL66NR -> OL69NR : 20 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536597",  # OL66NR -> OL69NR : 22 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536598",  # OL66NR -> OL69NR : 24 Albemarle Street, Ashton-under-Lyne, Lancashire
            "100011536599",  # OL66NR -> OL69NR : 26 Albemarle Street, Ashton-under-Lyne, Lancashire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200004419184",  # SK153AD -> SK153AE : 8C Portland Place, Mottram Road, Stalybridge, Cheshire
            "10090073715",  # OL66LX -> OL67TX : Flat 9, 213 Mossley Road, Ashton-under-Lyne, Lancashire
        ]:
            rec["accept_suggestion"] = False

        return rec


# Ambiguous, do nothing so they are disguarded.
# "10090075402",  # M437PU -> M437ZA : 1 Bridgewater House, Somerset Road, Droylsden, Manchester
# "10090075327",  # M437PU -> M437ZA : 2 Bridgewater House, Somerset Road, Droylsden, Manchester
# "10090075403",  # M437PU -> M437ZA : 3 Bridgewater House, Somerset Road, Droylsden, Manchester
# "10090075328",  # M437PU -> M437ZA : 4 Bridgewater House, Somerset Road, Droylsden, Manchester
# "10090075404",  # M437PU -> M437ZA : 5 Bridgewater House, Somerset Road, Droylsden, Manchester
# "10090075329",  # M437PU -> M437ZA : 6 Bridgewater House, Somerset Road, Droylsden, Manchester
# "200004409564",  # OL79DR -> OL79AA : Flat 1 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004409565",  # OL79DR -> OL79AA : Flat 2 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004424803",  # OL79DR -> OL79AA : Flat 3 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004409566",  # OL79DR -> OL79AA : Flat 4 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004424804",  # OL79DR -> OL79AA : Flat 5 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004409568",  # OL79DR -> OL79AA : Flat 6 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004409569",  # OL79DR -> OL79AA : Flat 7 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004424805",  # OL79DR -> OL79AA : Flat 8 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004409570",  # OL79DR -> OL79AA : Flat 9 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004409571",  # OL79DR -> OL79AA : Flat 10 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
# "200004424812",  # OL79DR -> OL79AA : Flat 11 The Raynors, Taunton Road, Ashton-under-Lyne, Lancashire
