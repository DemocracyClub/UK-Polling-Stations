from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000221"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Stratford.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Stratford.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id in ["7107", "7371", "7361", "7309", "7080"]:
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023584426",  # B496PA -> CV364LS : Meadowcroft, Croft Lane, Temple Grafton, Alcester
            "10091198673",  # CV370BJ -> B504GE : 23 Canners Way, Stratford-upon-Avon
            "10093540958",  # B504GT -> CV378US : 48 Spearhead Road, Bidford-on-Avon, Alcester
            "10093540959",  # B504GT -> CV378US : 50 Spearhead Road, Bidford-on-Avon, Alcester
            "10093540960",  # B504GT -> CV378US : 52 Spearhead Road, Bidford-on-Avon, Alcester
            "10093540962",  # B504GQ -> CV378US : 1 Arrow Way, Bidford-on-Avon, Alcester
            "10093540963",  # B504GQ -> CV378US : 3 Arrow Way, Bidford-on-Avon, Alcester
            "10093540964",  # B504GQ -> CV378US : 5 Arrow Way, Bidford-on-Avon, Alcester
            "10093540965",  # B504GQ -> CV378US : 7 Arrow Way, Bidford-on-Avon, Alcester
            "10093540966",  # B504GQ -> CV378US : 9 Arrow Way, Bidford-on-Avon, Alcester
            "10093540967",  # B504GQ -> CV378US : 11 Arrow Way, Bidford-on-Avon, Alcester
            "10093540968",  # B504GQ -> CV378US : 15 Arrow Way, Bidford-on-Avon, Alcester
            "10093540969",  # B504GQ -> CV378US : 17 Arrow Way, Bidford-on-Avon, Alcester
            "10093540970",  # B504GQ -> CV378US : 2 Arrow Way, Bidford-on-Avon, Alcester
            "10091198668",  # CV472RD -> B504GE : 1 Gaydon Road, Bishops Itchington, Southam
            "10024063184",  # CV365JB -> CV365PQ : The Cottage, The Old Rectory, Whichford, Shipston-on-Stour
            "100071246878",  # CV370AH -> CV378LW : Y-Not, Western Road, Stratford-upon-Avon
            "10024062702",  # CV376PT -> CV376PG : Flat 2, 6 Henley Street, Stratford-upon-Avon
            "10024632297",  # CV376DQ -> CV472AB : 26 Holtom Street, Stratford-upon-Avon
            "10091200519",  # CV376PQ -> CV364FH : 73 Albany Road, Stratford-upon-Avon
            "10091202963",  # CV376HS -> CV350EQ : 10 Broad Walk, Stratford-upon-Avon
            "10024635861",  # B956AE -> CV378WQ : 1 Henley Grange, Stratford Road, Henley-in-Arden
            "100071512443",  # CV359DB -> CV359BX : Westfields Stables, Moreton Morrell, Warwick
            "10093538940",  # CV350BF -> CV472BQ : 3 Gardiner Road, Kineton, Warwick
            "10023382712",  # B956JD -> B956JS : 1 The Gables, Brook Road, Aston Cantlow, Henley-in-Arden
            "10023582102",  # B496LZ -> B496HA : Kinwarton House, Kinwarton, Alcester
            "10023588987",  # B956JX -> B956JS : Hawthorne Cottage, Wheathills Farm, Aston Cantlow, Henley-in-Arden
            "10024635928",  # B496FH -> CV378WR : 3 Wakefield Way, Alcester
            "200001850488",  # B496LZ -> B496LY : Walcote Manor, Walcote, Alcester
            "10023384519",  # CV479PY -> CV479PX : Elm House, Marton Road, Long Itchington, Southam
            "10023382717",  # CV479PG -> CV478PG : 2 Poplar Gardens, Poplar Road, Napton on the Hill, Southam
            "10023382721",  # CV479PG -> CV478PG : 6 Poplar Gardens, Poplar Road, Napton on the Hill, Southam
            "10091201627",  # CV477SU -> B495DS : Beechwood Cottage, Nedge Hill Farm, Southam Road, Priors Marston, Southam
            "10024635977",  # CV364JN -> CV378WY : 1 Council Houses, Admington, Shipston-on-Stour
            "10024635978",  # CV364JN -> CV378WY : The Coach House Admington Hall, Admington, Shipston-on-Stour
            "10024635979",  # CV364JN -> CV378WY : 2 Council Houses, Admington, Shipston-on-Stour
            "10024635981",  # CV364JN -> CV378WY : Field View, Admington, Shipston-on-Stour
            "10024635982",  # CV364JN -> CV378WY : Nut Hatch, Admington, Shipston-on-Stour
            "10024635983",  # CV364JL -> CV378WY : Top Farm, Admington, Shipston-on-Stour
            "10024635984",  # CV364JN -> CV378WY : Gardenia Cottage, Admington, Shipston-on-Stour
            "10024636077",  # CV378WD -> CV364NT : 37 Wellington Avenue, Meon Vale, Stratford-upon-Avon
            "10091200357",  # CV378WP -> CV378NN : 25 Western Heights Road, Meon Vale, Stratford-upon-Avon
            "10023385159",  # CV472AQ -> CV472AE : Hillside Farm, Avon Dassett, Southam
            "10091198670",  # CV350DY -> B504GE : Barn at Tysoe Vale Farm, Tysoe Road, Kineton, Warwick
            "10091198671",  # CV350DY -> B504GE : Bungalow at Tysoe Vale Farm, Tysoe Road, Kineton, Warwick
            "200001854641",  # CV350QR -> CV350RH : The Barn, Kineton Road, Oxhill, Warwick
            "100071247719",  # CV370QN -> CV370QE : Four Gables, August Hill, Ingon Lane, Snitterfield, Stratford-upon-Avon
            "100071248808",  # CV370PF -> CV370PY : Stratford Manor Hotel, Warwick Road, Stratford-upon-Avon
            "10091203009",  # CV470JJ -> CV376UE : 60 Tithe Lodge, Little Park, Southam
            "10024632130",  # CV470HZ -> B955FE : 65 Manders Croft, Southam
            "10024635860",  # CV470HE -> CV378WQ : Flat 1, 6 Market Hill, Southam
            "10091202049",  # CV472TU -> CV370QF : 7 Swift Gardens, Southam
            "10024064222",  # B807HY -> CV364JQ : 45 St. Judes Avenue, Studley
            "100070215185",  # B807NP -> CV379DP : 94 Alcester Road, Studley
            "10023584458",  # B807PA -> CV365LW : 188 Alcester Road, Studley
            "100070221287",  # CV378JW -> CV378JX : 3 Station Road, Milcote, Stratford-upon-Avon
            "100070221288",  # CV378JW -> CV378JX : 4 Station Road, Milcote, Stratford-upon-Avon
            "100070221289",  # CV378JW -> CV378JX : 5 Station Road, Milcote, Stratford-upon-Avon
            "100070221290",  # CV378JW -> CV378JX : 6 Station Road, Milcote, Stratford-upon-Avon
            "100071246856",  # CV378LN -> CV378JT : Bard Cottage, Willicote Pastures, Campden Road, Clifford Chambers, Stratford-upon-Avon
            "100071514404",  # CV378RG -> CV378RA : End Cottage, Long Marston, Stratford-upon-Avon
            "100071514617",  # CV378RD -> CV378RA : The Willows, Long Marston, Stratford-upon-Avon
            "10023385569",  # CV378JW -> CV378LR : Lockes Barn, Station Road, Milcote, Stratford-upon-Avon
            "10023588333",  # CV378FH -> CV378HF : 3 Long Cast Park, Hunt Hall Lane, Welford-on-Avon, Stratford-upon-Avon
            "10091200358",  # CV378WP -> CV378NN : 26 Western Heights Road, Meon Vale, Stratford-upon-Avon
            "10091201630",  # CV379EJ -> CV378EJ : Keytes House, Church Street, Welford-on-Avon, Stratford-upon-Avon
            "10093539197",  # CV378QW -> CV479AP : 40 Bailey Avenue, Meon Vale, Stratford-upon-Avon
            "100071249386",  # CV350AA -> CV350AE : Bromson Hollow, Banbury Road, Ashorne, Warwick
        ]:
            rec["accept_suggestion"] = True
        if uprn in [
            "10024063650"  # B956DJ -> B496DJ : The Studio, Cutlers Farm, Edstone, Wootton Wawen, Henley-in-Arden
            "10023584948"  # CV376QQ -> CV376HE : Staff House, The Stratford Victoria, Alcester Road, Stratford-upon-Avon
        ]:
            rec["accept_suggestion"] = False

        return rec
