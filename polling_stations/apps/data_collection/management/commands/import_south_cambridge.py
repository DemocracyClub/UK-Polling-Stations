from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000012"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7342":
            record = record._replace(polling_place_postcode="CB8 0XF")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["200001850767", "10091623496", "10091623497", "10091624790"]:
            rec["postcode"] = "CB234NL"
            rec["accept_suggestion"] = False

        if uprn in ["100091203868"]:
            return None

        if uprn in [
            "10003188510",  # CB259NW -> CB259PG : 1 Goose Hall Farm, Ely Road, Waterbeach, Cambridge
            "10003183888",  # CB259PH -> CB259PW : School Farm House, Ely Road, Chittering, Cambridge
            "10033037257",  # CB231AA -> CB231NF : 13 Wisbey`s Yard, Haslingfield, Cambridge
            "10033037258",  # CB231AA -> CB231NF : 14 Wisbey`s Yard, Haslingfield, Cambridge
            "10033037259",  # CB231AA -> CB231NF : 15 Wisbey`s Yard, Haslingfield, Cambridge
            "10033037260",  # CB231AA -> CB231NF : 16 Wisbey`s Yard, Haslingfield, Cambridge
            "100091204382",  # CB227NJ -> CB227NH : 2 New Farm, Royston Road, Harston, Cambridge
            "100091204381",  # CB227NJ -> CB227NH : 1 New Farm, Royston Road, Harston, Cambridge
            "10003195547",  # CB223AY -> CB223AE : Magog House, Cambridge Road, Babraham, Cambridge
            "10003193988",  # SG85JR -> SG85JS : Calvisi, Old North Road, Bassingbourn, Royston
            "10008082645",  # SG85JR -> SG85SR : Flat 4 Taunus, Old North Road, Bassingbourn, Royston
            "10008080949",  # SG85JR -> SG85SR : Flat 2 Taunus, Old North Road, Bassingbourn, Royston
            "10003193066",  # SG80QN -> SG85NT : St. Johnsbury, Bassingbourn Road, Litlington, Royston
            "10003195581",  # SG80HP -> SG80HT : Penquite, Flecks Lane, Wendy Road, Shingay-Cum-Wendy, Royston
            "10003202065",  # CB223XE -> CB223EH : Roxborough, 2A Brookfield Road, Sawston, Cambridge
            "100091202269",  # CB225ED -> CB225BP : Stapleford Grange, Stapleford, Cambridge
            "10003182031",  # CB89LD -> CB89LE : 171 Carlton Green Road, Carlton, Newmarket
            "10003182035",  # CB89LD -> CB89LE : Rood Hall, Carlton Green Road, Carlton, Newmarket
            "100091204465",  # CB215NE -> CB215PF : Wadlow Farm House, Six Mile Bottom Road, West Wratting, Cambridge
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100090161038"  # CB237XA -> CB227AD : 10 The Pastures, Hardwick, Cambridge
        ]:
            rec["accept_suggestion"] = False

        return rec
