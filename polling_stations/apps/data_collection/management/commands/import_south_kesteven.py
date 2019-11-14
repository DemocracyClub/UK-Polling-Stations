from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000141"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019SK.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019SK.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10007252542":
            rec["postcode"] = "NG32 3NG"

        if uprn == "10007257471":
            rec["postcode"] = "NG34 0NJ"

        if uprn == "10007257235":
            rec["postcode"] = "PE9 4NT"

        if record.post_code in ("NG31 8NH",):
            # Assigned polling station looks a bit suss
            return None

        if uprn in [
            "100030920062",  # NG321LT -> NG321LD : Bullimore`s Cottage, 89 Main Street, Denton, Grantham, Lincs
            "10007253051",  # NG321AT -> NG321AN : The Corner Cottage, 5 Hungerton Hollow, Grantham, Lincs
            "10007246148",  # NG321LT -> NG321LY : 42 Main Street, Woolsthorpe-By-Belvoir, Grantham, Lincs
            "100032120092",  # NG321NW -> NG321LT : Anvil Cottage, Main Street, Woolsthorpe-By-Belvoir, Grantham, Lincs
            "10007246156",  # NG321LX -> NG321LT : Hillside, 21 Main Street, Woolsthorpe-By-Belvoir, Grantham, Lincs
            "10007246168",  # NG321LX -> NG321LT : The Hollies, Main Street, Woolsthorpe-By-Belvoir, Grantham, Lincs
            "10007252200",  # PE69SF -> PE69NG : Stowe Farm, Langtoft, Peterborough
            "100030933880",  # PE68EW -> PE68EN : 22 Horsegate, Deeping St James, Peterborough
            "10007252327",  # PE94AP -> PE94PE : Old Hall Farmhouse, Main Street, Wilsthorpe, Stamford, Lincs
            "10007252351",  # PE94PE -> PE94DT : Mill Farm, Holywell, Stamford, Lincs
            "10007248918",  # NG334JQ -> NG334QB : The Old Rectory, Church Lane, Creeton, Grantham, Lincs
            "10007263316",  # NG319JZ -> NG316JZ : Flat 4 Market View, 61-62 Westgate, Grantham, Lincs
            "10007246209",  # NG334HE -> NG334DH : Shangri-La, Ponton Road, Boothby Pagnell, Grantham, Lincs
            "100030918020",  # NG323AU -> NG322AU : Cornerway, Hough Road, Brandon, Grantham, Lincs
            "100030936930",  # PE68LQ -> PE68GD : Karamanda, 80 Towngate East, Market Deeping, Peterborough
            "100030933837",  # PE68EB -> PE68ED : The Laurels Residential Home, 45 High Street, Market Deeping, Peterborough
            "10007247477",  # NG323AU -> NG323AP : Glenville, Main Street, Carlton Scroop, Grantham, Lincs
            "10007252178",  # NG323AY -> NG323SB : 4 Main Street, Sudbrook, Grantham, Lincs.
            "100030919971",  # NG322LW -> NG322NH : Corner House, Main Road, Barkston, Grantham, Lincs
            "10007242167",  # NG322DU -> NG322EF : Willow Top Farm, Gonerby Lane, Allington, Grantham, Lincs
            "10007246399",  # NG334SP -> NG334SR : The Barn, Porters Lodge Farm, Morkery Lane, Castle Bytham, Grantham, Lincs.
            "100030904285",  # PE109AE -> PE109EA : Flat Over Bank, R/o 4 North Street, Bourne, Lincs
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10007248507",  # NG321LH -> NG318BY : Park Cottage, Park Lane, Denton, Grantham, Lincs
            "200001873982",  # PE91QP -> PE91QL : Hazel Grove, Emlyns Street, Stamford, Lincs
            "10007257592",  # PE100TT -> PE100TG : Gatehouse Cottage, Fen Road, Dowsby, Bourne, Lincs
        ]:
            rec["accept_suggestion"] = False

        return rec
