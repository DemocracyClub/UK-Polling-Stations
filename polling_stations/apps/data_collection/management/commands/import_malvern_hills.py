from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000235"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019malv.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019malv.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10014094039", "10014094040"]:
            return None

        if uprn == "10014091874":
            rec["postcode"] = "DY13 0SQ"

        if uprn == "10024319007":
            rec["postcode"] = "WR2 4SF"

        if uprn == "10014091918":
            rec["postcode"] = "DY13 0SQ"

        if uprn in [
            "10014093545",  # WR158QY -> WR158QW : Garwood Cottage, Hanley Childe, Tenbury Wells, Worcestershire
            "10024319833",  # WR136AE -> WR136AF : Rye Cross Garage, Birtsmorton, Malvern, Worcestershire
            "10014090705",  # WR158QY -> WR158QN : The Bungalow, Hill Farm, Hanley Childe, Tenbury Wells, Worcestershire
            "10014094354",  # WR158QY -> WR158SR : Hollywall, Hanley Childe, Tenbury Wells, Worcestershire
            "10014090711",  # WR158QY -> WR158QW : The Mathons, Hanley Childe, Tenbury Wells, Worcestershire
            "10014087209",  # WR158TA -> WR158TB : High Croft, 1 Callows Meadow, Tenbury Wells, Worcestershire
            "10014091220",  # WR66UA -> WR66UB : Lowe Green Cottage, Lowe Green, Stockton, Worcester
            "10014087210",  # WR158TA -> WR158TB : 2 Callows Meadow, Tenbury Wells, Worcestershire
            "10014087212",  # WR158TA -> WR158TB : 4 Callows Meadow, Tenbury Wells, Worcestershire
            "10014093991",  # WR158JE -> WR158JF : The Ferns, Newnham Bridge, Tenbury Wells, Worcestershire
            "100120594638",  # WR158DP -> WR158TB : Ponderosa, Oldwood Road, Tenbury Wells, Worcestershire
            "10014089920",  # DY149HX -> DY149JL : Chimneys, Mamble, Kidderminster, Worcestershire
            "10014092506",  # WR66ST -> WR66SJ : Grovewood House, Stanford Bridge, Worcester
            "100120596005",  # WR66JB -> WR66JP : St. Michaels Farm, Great Witley, Worcester
            "10014091421",  # WR65PA -> WR65NX : Devils Leap Cottage, Devils Leap, Broadwas, Worcester
            "10014086840",  # WR80DN -> WR80EQ : The Old Dairy, Horton Manor Farm, Hanley Swan, Worcester
            "10014089048",  # WR53PE -> WR53PF : Durridge House, Kerswell Green, Kempsey, Worcester
            "10000831211",  # WR158TB -> WR158PN : Oldwood Farm, Oldwood, Tenbury Wells, Worcestershire
            "100121267960",  # WR158TA -> WR158TD : Littledean, Oldwood Road, Tenbury Wells, Worcestershire
            "10014090750",  # WR158QJ -> WR158QN : Woodstock Bower Farm, Stoke Bliss, Tenbury Wells, Worcestershire
            "10014090027",  # WR66YY -> WR66XY : The Bungalow, Hill Farm, Wichenford, Worcester
            "10014091996",  # WR66YG -> WR66YS : Kings Green Farm, Kings Green, Wichenford, Worcester
            "200002874926",  # WR135AJ -> WR135AQ : Madresfield Grange, Madresfield, Malvern, Worcestershire
            "200003224371",  # WR26RH -> WR26RL : Jenya, Crown East Lane, Lower Broadheath, Worcester
            "10024317453",  # WR65NE -> WR65NR : Blackfields Cottage, Broadwas, Worcester
            "100120595755",  # WR66QL -> WR66QJ : Spring Meadow, Quarry Lane, Martley, Worcester
            "100120594930",  # WR25TU -> WR25TR : Parkfield, Crown East, Worcester
            "100120595357",  # WR53PA -> WR53PB : Mereside, Main Road, Kempsey, Worcester
            "10014088389",  # WR66LX -> WR66LF : The Stables, Dingle Court, Little Witley, Worcester
            "100120605457",  # WR144LB -> WR144LD : Brook House, 197 Upper Welland Road, Malvern Wells, Worcestershire
            "100121268065",  # WR24SL -> WR24SW : Deadfields, Bastonford, Powick, Worcester
            "200001124444",  # WR80PS -> WR80PL : 2 Ryall Grove, Upton-Upon-Severn, Worcester
            "200003221308",  # WR80BB -> WR80AT : The New House, Brotheridge Green, Hanley Castle, Worcester
            "200001728481",  # WR80AY -> WR80AU : Hill View, Hook Bank, Hanley Castle, Worcester
            "10000830296",  # WR142LU -> WR141LU : 15 Peak View, Yates Hay Road, Malvern, Worcestershire
            "200003225404",  # WR66QW -> WR65QW : Upper Barn, Ravenhall Farm, Lulsley, Knightwick, Worcester
            "100121268164",  # WR22TZ -> WR24TZ : The Lodge, 36 Upton Road, Callow End, Worcester
            "10024319122",  # WR143BA -> WR143AN : Poulton House, Malvern Girls College, Avenue Road, Malvern, Worcestershire
            "100120595370",  # WR22SN -> WR24SN : Ridgeway Barn, Malvern Road, Bastonford, Powick, Worcester
            "10024317597",  # WR158JE -> WR158JF : Garden Cottage, Newnham Court, Newnham Bridge, Tenbury Wells, Worcestershire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10024318867",  # DY130RY -> WR24RY : Hampstall Inn, Hampstall Lane, Astley Burf, Stourport on Severn, Worcestershire
            "10024321881",  # WR66BF -> WR142BT : 6 Ryecroft Way, Martley, Worcester
            "10024321732",  # WR158TQ -> WR66YE : Hawk Cabin, Cadmore Lodge, Berrington Green, Tenbury Wells, Worcestershire
            "10093062462",  # WR136JW -> WR135FB : 65 Three Counties Park, Upper Pendock, Malvern, Worcestershire
            "10093062122",  # WR53JN -> WR143HL : Little Orchard, 25A Lyf's Lane, Kempsey, Worcester
            "10000832472",  # DY130RR -> WR66PN : The Old Court, Astley, Stourport on Severn, Worcestershire
        ]:
            rec["accept_suggestion"] = False

        return rec
