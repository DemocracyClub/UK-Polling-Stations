from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000139"
    addresses_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019 revised file.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019 revised file.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10006541667":
            return None

        if uprn in [
            "10006530403",  # NG348HB -> NG348HH : York House Officers Mess, R A F College, Cranwell, Sleaford
            "10006510362",  # LN41DJ -> LN41JD : Brinkle Springs, Acre Dyke Lane, Heighington, Lincoln
            "10006510378",  # LN41JG -> LN41JQ : Timperley, Bardney Road, Branston Booths, Lincoln
            "10006505994",  # LN43RA -> LN43RR : North Moor Farm, Linwood Road, Martin, Lincoln
            "10006507278",  # NG340BU -> NG340BN : Hill Top Farmhouse, Burton Gorse, Sleaford, Lincs
            "10006515656",  # LN50DW -> LN50BN : Devonshire Grange, The Heath, Wellingore, Lincoln
            "10006522464",  # LN44BB -> LN44BL : 1 the Hurn, Parsons Drove, Billinghay, Lincoln
            "10006527563",  # LN106XJ -> LN106XL : New Road Farm, Blankney Dales, Woodhall Spa, Lincs
            "10006527907",  # PE203QF -> PE203PZ : Rakes Farm, Swineshead Bridge, Boston
            "10006529717",  # LN50SS -> LN50SR : 1 the Cottages Carlton Lowfield Farm, Brant Broughton, Carlton Le Moorland, Lincoln
            "10006529720",  # LN50SS -> LN50SR : 2 the Cottages Carlton Lowfield Farm, Brant Broughton, Carlton Le Moorland, Lincoln
            "10006529962",  # LN44BW -> LN44BP : Lowe`s Dwelling, Tattershall Road, Billinghay, Lincoln
            "10006530120",  # PE203QF -> PE203QA : Mobile Home, Maize Farm, East Heckington, Boston, Lincs
            "10006534005",  # LN44JL -> LN44JW : Chapel Bungalow Tattershall Bridge Road, Tattershall Bridge, Lincoln
            "10006536127",  # NG340DA -> NG340BN : Fir Nature, White Cross Lane, Burton Pedwardine, Sleafordorpe, Lincoln
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001146077",  # NG348HB -> NG348EL : Daedalus Officers Mess, R A F College, Cranwell, Sleaford
            "10006506295",  # LN43LT -> LN43JF : 1 Church End, Rowston, Lincoln
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "5879":  # Washingborough Community Centre
            record = record._replace(polling_place_easting="502596")
            record = record._replace(polling_place_northing="370730")

        if record.polling_place_id == "5993":  # Sleaford Leisure Centre
            record = record._replace(polling_place_easting="507252")
            record = record._replace(polling_place_northing="345802")

        return super().station_record_to_dict(record)
