from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000125"
    addresses_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019 Rossendale.TSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019 Rossendale.TSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100010597181":
            return None

        if uprn in [
            "10013834533",  # OL130QR -> OL138GB : 24 Deerplay Drive, Weir, Bacup, Lancs
            "10013834535",  # OL130QR -> OL138GB : 26 Deerplay Drive, Weir, Bacup, Lancs
            "100012409974",  # OL138RQ -> OL138PF : Sunny Croft, Causeway Head, Off Burnley Road, Broad Clough, Bacup, Lancashire
            "100012409973",  # OL138RQ -> OL138PF : Holmlea, Causeway Head, Off Burnley Road, Broad Clough, Bacup, Lancashire
            "10013834534",  # OL130QR -> OL138GB : 25 Deerplay Drive, Weir, Bacup, Lancs
            "10013834536",  # OL130QR -> OL138GB : 27 Deerplay Drive, Weir, Bacup, Lancs
            "100010597181",  # OL138EX -> OL130EX : Flat Over, 15 Market Street, Bacup, Lancs
            "100012732873",  # OL130JL -> OL130PS : Moss Farm, Blackwood Road, Stacksteads, Bacup, Lancs
            "100012409952",  # OL139XB -> OL139WU : The Bungalow, Railgate, Off Tong Lane, Britannia, Bacup, Lancs
            "100012733254",  # OL139SB -> OL139SA : Dean Holme, Deansgreave Road, Bacup, Lancashire
            "100012411007",  # BB48TT -> BB48RR : Old Hall Farm, Haslingden Old Road, Rawtenstall, Rossendale, Lancashire
            "10013836714",  # BB47JH -> BB47AF : Middle Lench Farm, Lench Road, Waterfoot, Rossendale, Lancashire
            "100010605533",  # BB49HT -> BB49HU : 270 Burnley Road East, Waterfoot, Rossendale, Lancashire
            "100012410487",  # BB49BQ -> BB49BD : The Jolly Sailor, Booth Road, Waterfoot, Rossendale, Lancashire
            "100010607020",  # BB47TD -> BB49TD : 51 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607024",  # BB47TD -> BB49TD : 53 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607004",  # BB47TD -> BB49TD : 43A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607015",  # BB47TD -> BB49TD : 49A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607036",  # BB47TD -> BB49TD : 59 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607040",  # BB47TD -> BB49TD : 61 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607031",  # BB47TD -> BB49TD : 57A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607005",  # BB47TD -> BB49TD : 43 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607012",  # BB47TD -> BB49TD : 47 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607019",  # BB47TD -> BB49TD : 51A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607028",  # BB47TD -> BB49TD : 55 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "10013836328",  # BB49ND -> BB49NE : Lower Walls Farm, Walls Clough, Lumb, Rossendale
            "10014330321",  # OL130TH -> OL130BF : Fearns School House, Booth Road, Waterfoot, Rossendale, Lancashire
            "100010607032",  # BB47TD -> BB49TD : 57 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010606999",  # BB47TD -> BB49TD : 39 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607008",  # BB47TD -> BB49TD : 45 Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607011",  # BB47TD -> BB49TD : 47A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607023",  # BB47TD -> BB49TD : 53A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010606996",  # BB47TD -> BB49TD : 37/37A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010606998",  # BB47TD -> BB49TD : 39A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607027",  # BB47TD -> BB49TD : 55A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607035",  # BB47TD -> BB49TD : 59A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010602662",  # OL128NU -> OL128NP : 56 Oak Street, Whitworth, Rochdale, Lancashire
            "100010607039",  # BB47TD -> BB49TD : 61A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "100010607007",  # BB47TD -> BB49TD : 45A Crabtree Avenue, Waterfoot, Rossendale, Lancashire
            "200002827316",  # BB49TF -> BB49DQ : Walker, Wales House, Wales Road, Waterfoot, Rossendale, Lancashire
            "10014330366",  # BB49NE -> BB49PG : The Gate House, Lower Wheathead Farm, Walls Clough, Off Burnley Road East, Lumb, Rossendale
            "200001909469",  # BB49LR -> BB49RT : Shadlock Cote House, West View Road, Whitewell Bottom, Rossendale, Lancashire
            "100012732210",  # OL128BH -> OL128BQ : 10 Sandbank Cottages, Whitworth, Rochdale, Lancashire
            "100012410120",  # OL128BH -> OL128BQ : 14 Sandbank Cottages, Whitworth, Rochdale, Lancashire
            "100012410121",  # OL128BH -> OL128BQ : 16 Sandbank Cottages, Whitworth, Rochdale, Lancashire
            "100012411006",  # BB48TT -> BB48RR : Old Hall Barn, Haslingden Old Road, Rawtenstall, Rossendale, Lancashire
            "10014332391",  # OL139QA -> OL138QA : 2 Weir Lane, Weir, Bacup, Lancs
            "10014331922",  # BB48UE -> BB48UD : Laund Farm Barn, Cribden Lane, Crawshawbooth, Rossendale
            "100012733067",  # OL139BT -> OL138RQ : 4 Lane Head Farm, Bacup Old Road, Bacup, Lancashire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100012410247",
            "100010605454",
            "100010605455",
            "100010605456",
        ]:
            rec["accept_suggestion"] = False

        return rec
