from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000031"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Wolves.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Wolves.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "24941":
            record = record._replace(polling_place_postcode="")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.170782770209159, 52.57045225795353, srid=4326)
            return rec

        rec = super().station_record_to_dict(record)
        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() == "VW2 1FA":
            rec["postcode"] = "WV2 1FA"

        if record.addressline6.strip() == "WV14 8UT":
            return None

        if uprn == "10033911488":
            rec["postcode"] = "WV14 0SD"

        if record.addressline6 == "WV14 6NR":
            return None

        if uprn == "10090643532":
            rec["postcode"] = "WV4 6BE"

        if uprn in [
            "100071124886",  # WV147HT -> WV147EY : 34 Lunt Road, Lunt, Bilston, West Midlands
            "100071124888",  # WV147HT -> WV147EY : 36 Lunt Road, Lunt, Bilston, West Midlands
            "100071124895",  # WV147HT -> WV147EY : 52 Lunt Road, Lunt, Bilston, West Midlands
            "100071124897",  # WV147HT -> WV147EY : 54 Lunt Road, Lunt, Bilston, West Midlands
            "10090640337",  # WV21AA -> WV24AD : Chaplains Flat St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012791",  # WV21AA -> WV24AD : Flat 1 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012792",  # WV21AA -> WV24AD : Flat 2 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012793",  # WV21AA -> WV24AD : Flat 3 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012794",  # WV21AA -> WV24AD : Flat 4 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012795",  # WV21AA -> WV24AD : Flat 5 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012796",  # WV21AA -> WV24AD : Flat 6 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012797",  # WV21AA -> WV24AD : Flat 7 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012798",  # WV21AA -> WV24AD : Flat 8 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012799",  # WV21AA -> WV24AD : Flat 9 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012800",  # WV21AA -> WV24AD : Flat 10 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012801",  # WV21AA -> WV24AD : Flat 11 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012802",  # WV21AA -> WV24AD : Flat 12 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012803",  # WV21AA -> WV24AD : Flat 13 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012804",  # WV21AA -> WV24AD : Flat 14 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012805",  # WV21AA -> WV24AD : Flat 15 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012806",  # WV21AA -> WV24AD : Flat 16 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012807",  # WV21AA -> WV24AD : Flat 17 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012808",  # WV21AA -> WV24AD : Flat 18 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012809",  # WV21AA -> WV24AD : Flat 19 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012810",  # WV21AA -> WV24AD : Flat 20 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012811",  # WV21AA -> WV24AD : Flat 21 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012812",  # WV21AA -> WV24AD : Flat 22 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "10090012813",  # WV21AA -> WV24AD : Flat 23 St. Mary`s Hall, Tempest Street, Wolverhampton, West Midlands
            "100071351215",  # WV146NL -> WV146NW : Ground Floor Flat, 66 Willenhall Road, Bilston, West Midlands
            "10090013527",  # WV21AA -> WV12AA : 302B Deans Road, East Park, Wolverhampton, West Midlands
            "100071198253",  # WV108NJ -> WV108LJ : 58 Tennyson Road, Scotlands, Wolverhampton, West Midlands
            "10007124478",  # WV111RG -> WV111RH : First Floor Flat, 312 Prestwood Road, Heath Town, Wolverhampton, West Midlands
            "100071202129",  # WV113JS -> WV113SJ : 140 Waddensbrook Lane, Wednesfield, Wolverhampton, West Midlands
            "100071175970",  # WV113UQ -> WV113QU : 76 March End Road, Wednesfield, Wolverhampton, West Midlands
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100071152232",  # WV22EU -> WV100SG : 1 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152233",  # WV22EU -> WV100SG : 2 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152234",  # WV22EU -> WV100SQ : 3 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152235",  # WV22EU -> WV100SG : 4 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152236",  # WV22EU -> WV100SQ : 5 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152237",  # WV22EU -> WV100SG : 6 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152238",  # WV22EU -> WV100SQ : 7 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152239",  # WV22EU -> WV100SG : 8 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152240",  # WV22EU -> WV100SQ : 9 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152241",  # WV22EU -> WV100SQ : 10 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "100071152242",  # WV22EU -> WV100SQ : 11 D`urberville Close, Rough Hills, Wolverhampton, West Midlands
            "10093326112",  # WV140HX -> WV23EW : 8A Talbot Place, Bilston, West Midlands
            "10093326113",  # WV140HX -> WV23EW : 8B Talbot Place, Bilston, West Midlands
            "100071143501",  # WV108QG -> WV100BH : 314 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143502",  # WV108QG -> WV100BH : 316 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143503",  # WV108QG -> WV100BH : 318 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143504",  # WV108QG -> WV100BH : 320 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143505",  # WV108QG -> WV100BH : 322 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143506",  # WV108QG -> WV100BH : 324 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143507",  # WV108QG -> WV100BH : 326 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143508",  # WV108QG -> WV100BH : 328 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143509",  # WV108QG -> WV100BH : 330 Cannock Road, Westcroft, Westcroft, Wolverhampton, West Midlands
            "100071143573",  # WV108PW -> WV100AE : Flat, 92 Cannock Road Wednesfield*
            "100071143574",  # WV108PW -> WV100AE : First Floor, 94 Cannock Road Wednesfield*
            "100071556685",  # WV100HX -> WV100LG : 56 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556693",  # WV100HX -> WV100JG : 64 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556698",  # WV100HX -> WV100NF : 69 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556703",  # WV100HX -> WV100RA : 74 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556704",  # WV100HX -> WV100RA : 75 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556705",  # WV100HX -> WV100RA : 76 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556706",  # WV100HX -> WV100RA : 77 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556707",  # WV100HX -> WV100RA : 78 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556708",  # WV100HX -> WV100RA : 79 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556710",  # WV100HX -> WV100RA : 81 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556711",  # WV100HX -> WV100RA : 82 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556712",  # WV100HX -> WV100UB : 83 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556713",  # WV100HX -> WV100UG : 84 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556719",  # WV100HX -> WV100NF : 90 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556720",  # WV100HX -> WV100NT : 91 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071556728",  # WV100HX -> WV13EB : 99 Longfield House, Tithe Croft, Wolverhampton, West Midlands
            "100071195306",  # WV106SP -> WV45QB : 2 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195307",  # WV106SP -> WV45QB : 4 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195308",  # WV106SP -> WV45QB : 6 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195309",  # WV106SP -> WV45QB : 8 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195310",  # WV106SP -> WV45QB : 10 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195311",  # WV106SP -> WV45QB : 12 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195312",  # WV106SP -> WV45QB : 14 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195313",  # WV106SP -> WV45QB : 16 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195314",  # WV106SP -> WV45QB : 18 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195315",  # WV106SP -> WV45QB : 20 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071195316",  # WV106SP -> WV45QB : 22 St. Anne`s Road, Fordhouses, Wolverhampton, West Midlands
            "100071207477",  # WV100BB -> WV111PL : 46 Woden Road, Heath Town, Wolverhampton, West Midlands
            "100071207478",  # WV100BB -> WV111PU : 47 Woden Road, Heath Town, Wolverhampton, West Midlands
            "100071207479",  # WV100BB -> WV111PL : 48 Woden Road, Heath Town, Wolverhampton, West Midlands
            "100071207480",  # WV100BB -> WV111PU : 49 Woden Road, Heath Town, Wolverhampton, West Midlands
            "100071373072",  # WV140AX -> WV30TT : Horse & Jockey, 72 Church Street, Bilston, West Midlands
            "10090013485",  # WV146BN -> WV146BP : 2 Cemetery Street, Bilston, West Midlands
            "100071356546",  # WV45ES -> WV39JQ : 114 Park Hall Road, Goldthorn Park, Wolverhampton, West Midlands
            "10090643975",  # WV12FA -> WV22BF : 2 Roland Elcock House, Barnfield Road, East Park, Wolverhampton, West Midlands
            "100071181466",  # WV12JR -> WV108ER : 345A Willenhall Road, Wolverhampton, West Midlands
            "10090642339",  # WV22BF -> WV12FA : 11 Kirkwall Crescent, Wolverhampton
            "10090010901",  # WV44PL -> WV11QU : 2 Kingsclere Walk, Merry Hill, Wolverhampton, West Midlands
            "10093325431",  # WV14LP -> WV109QY : Herian House, 11 Fold Street, Wolverhampton, West Midlands
            "10090012751",  # WV146NL -> WV12HG : Flat, 3 Willenhall Road, Bilston, West Midlands
            "100071350780",  # WV146DH -> WV146BZ : The Happy Wanderer, Green Lanes, Bilston, West Midlands
            "100071192196",  # WV108JG -> WV108JN : Homestead, Sandy Lane, Bushbury, Wolverhampton, West Midlands
            "100071557101",  # WV108BT -> WV108BN : East View, Old Fallings Lane, Fallings Park, Wolverhampton, West Midlands
            "10090642314",  # WV37AX -> WV146QU : First Floor Flat, 6A Hughes Avenue, Birches Barn, Wolverhampton, West Midlands
            "100071353305",  # WV38BB -> WV38BA : School House, Finchfield Road West, Finchfield, Wolverhampton, West Midlands
            "10093324259",  # WV38BB -> WV38BA : 78 Finchfield Road West, Finchfield, Wolverhampton, West Midlands
            "100071374695",  # WV44LR -> WV44LP : 54B Warstones Road, Penn, Wolverhampton, West Midlands
            "10007123820",  # WV39NJ -> WV60DE : Flat 14, 135/137 Tettenhall Road, Wolverhampton, West Midlands
            "100071351844",  # WV46NY -> WV46NZ : The Copper Bowl, 200 Birmingham New Road, Lanesfield, Wolverhampton, West Midlands
            "10007123304",  # WV11DG -> WV140AG : Flat, 14 Lichfield Street, Wolverhampton, West Midlands
            "10090013969",  # WV11NA -> WV106JT : Flat 1, 172A Stafford Street, Wolverhampton, West Midlands
        ]:
            rec["accept_suggestion"] = False

        return rec
