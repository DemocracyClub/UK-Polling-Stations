from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000139"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019kest.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019kest.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "latin-1"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10006530403",  # NG348HB -> NG348HH : York House Officers Mess, R A F College, Cranwell, Sleaford
            "10006510362",  # LN41DJ -> LN41JD : Brinkle Springs, Acre Dyke Lane, Heighington, Lincoln
            "10006510378",  # LN41JG -> LN41JQ : Timperley, Bardney Road, Branston Booths, Lincoln
            "10006526117",  # LN41JH -> LN41AE : Ronsway, Fen Road, Heighington, Lincoln
            "10006505994",  # LN43RA -> LN43RR : North Moor Farm, Linwood Road, Martin, Lincoln
            "10006507278",  # NG340BU -> NG340BN : Hill Top Farmhouse, Burton Gorse, Sleaford, Lincs
            "10006515656",  # LN50DW -> LN50BN : Devonshire Grange, The Heath, Wellingore, Lincoln
            "10006516242",  # LN41JA -> LN41HZ : Claremont, Moor Lane, Branston, Lincoln
            "10006522464",  # LN44BB -> LN44BL : 1 the Hurn, Parsons Drove, Billinghay, Lincoln
            "10006527563",  # LN106XJ -> LN106XL : New Road Farm, Blankney Dales, Woodhall Spa, Lincs
            "10006527907",  # PE203QF -> PE203PZ : Rakes Farm, Swineshead Bridge, Boston
            "10006529717",  # LN50SS -> LN50SR : 1 the Cottages Carlton Lowfield Farm, Brant Broughton, Carlton Le Moorland, Lincoln
            "10006529720",  # LN50SS -> LN50SR : 2 the Cottages Carlton Lowfield Farm, Brant Broughton, Carlton Le Moorland, Lincoln
            "10006529962",  # LN44BW -> LN44BP : Lowe`s Dwelling, Tattershall Road, Billinghay, Lincoln
            "10006530120",  # PE203QF -> PE203QA : Mobile Home, Maize Farm, East Heckington, Boston, Lincs
            "10006534005",  # LN44JL -> LN44JW : Chapel Bungalow Tattershall Bridge Road, Tattershall Bridge, Lincoln
            "10006536127",  # NG340DA -> NG340BN : Fir Nature, White Cross Lane, Burton Pedwardine, Sleaford
            "10006539008",  # LN50DP -> LN50DW : Walnut Tree Barn, Pottergate Road, Wellingore, Lincoln
            "10006527449",  # LN65UU -> LN68HB : 34A Lincoln Road, Skellingthorpe, Lincoln
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001146077",  # NG348HB -> NG348EL : Daedalus Officers Mess, R A F College, Cranwell, Sleaford
            "10006506295",  # LN43LT -> LN43JF : 1 Church End, Rowston, Lincoln
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "5063":
            record = record._replace(polling_place_easting="502596")
            record = record._replace(polling_place_northing="370730")

        if record.polling_place_id == "5181":
            record = record._replace(polling_place_postcode="NG34 7HH")
            record = record._replace(polling_place_easting="507252")
            record = record._replace(polling_place_northing="345802")

        return super().station_record_to_dict(record)
