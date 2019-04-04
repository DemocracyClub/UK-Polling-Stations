from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000030"
    addresses_name = "local.2019-05-02/Version 1/Swindon.CSV"
    stations_name = "local.2019-05-02/Version 1/Swindon.CSV"
    elections = ["local.2019-05-02"]

    def station_record_to_dict(self, record):

        if record.polling_place_id == "8564":
            record = record._replace(polling_place_postcode="SN4 0LS")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10093398297", "10093400685"]:
            return None

        if uprn in [
            "10008541867",  # SN40QH -> SN40QZ : Midge Hall, Hackpen, Swindon
            "10008543170",  # SN13AJ -> SN13AW : 28A Victoria Road, Swindon
            "10008547382",  # SN268BZ -> SN268DD : 2 Lower Widhill Farm Cottages, Blunsdon Hill, Swindon
            "100121127018",  # SN13HG -> SN13HU : Little London, 25A Cricklade Street, Swindon
            "100121168352",  # SN13HU -> SN13HG : 23A Little London, Swindon
            "100121168353",  # SN13HG -> SN13HU : 23 Cricklade Street, Swindon
            "100121343468",  # SN14BJ -> SN14BD : The Flat, 64 Devizes Road, Swindon
            "100121347155",  # SN67DF -> SN67DG : 17 Downs View, Highworth, Swindon
            "100121398906",  # SN22PD -> SN22PE : 347B Cheney Manor Road, Rodbourne Cheney, Swindon
            "10022786126",  # SN67JY -> SN67RB : Eversleigh, Pentylands Lane, Highworth, Swindon
            "10022786903",  # SN253JG -> SN254YX : Toby Carvery, Elstree Way, Abbey Meads, Swindon
            "10090042076",  # SN251TX -> SN251BQ : Bosworth House, flat 3 87 Havisham Drive, Swindon
            "10093399090",  # SN35EP -> SN36EP : 124 Homington Avenue, Swindon
            "200002925970",  # SN55PJ -> SN55PH : 33 Old Shaw Lane, Swindon
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10004845052",  # SN13NH -> SN13NE : 12 Folkestone Road, Swindon
            "10008543334",  # SN21HS -> SN13BD : 21 David Stoddart Gardens, Omdurman Street, Swindon
            "10008543357",  # SN21DB -> SN13BU : 40 Ipswich Street, Swindon
            "10008543358",  # SN21DB -> SN13BU : 29 Ipswich Street, Swindon
            "10008543359",  # SN21DB -> SN13BU : 19 Ipswich Street, Swindon
            "10008543360",  # SN21BW -> SN13BU : Bedsit 2, 37 Whiteman Street, Swindon
            "10008543361",  # SN21BW -> SN13BU : 29 Whiteman Street, Swindon
            "10008544449",  # SN67SG -> SN34QS : Beech Farm, Swindon Road, Stanton Fitzwarren, Swindon
            "10008544486",  # SN40EP -> SN40EU : The Bungalow, Plough Hill, Marlborough Road, Chiseldon, Swindon
            "10009418291",  # SN21BW -> SN28DN : 79 Whiteman Street, Swindon
            "10010426897",  # SN40QZ -> SN40QH : 8 Hackpen Cottage, Barbury Castle Road, Hackpen, Wroughton, Swindon
            "10010427313",  # SN34QL -> SN34SF : 47 Highworth Road, Stratton St Margaret, Swindon
            "100121132326",  # SN55AZ -> SN253NX : 3 Frith Copse, Swindon
            "100121132327",  # SN55AZ -> SN253NX : 4 Frith Copse, Swindon
            "100121132328",  # SN55AZ -> SN253NX : 5 Frith Copse, Swindon
            "100121132329",  # SN55AZ -> SN253NX : 6 Frith Copse, Swindon
            "100121132330",  # SN55AZ -> SN253NX : 7 Frith Copse, Swindon
            "100121132331",  # SN55AZ -> SN253NX : 8 Frith Copse, Swindon
            "100121132332",  # SN55AZ -> SN253NX : 9 Frith Copse, Swindon
            "100121132333",  # SN55AZ -> SN253NX : 10 Frith Copse, Swindon
            "100121132334",  # SN55AZ -> SN253NX : 11 Frith Copse, Swindon
            "100121132335",  # SN55AZ -> SN253NX : 12 Frith Copse, Swindon
            "100121167052",  # SN14AY -> SN14AS : Lindum House, 84 Bath Road, Swindon
            "100121363131",  # SN40RZ -> SN14BJ : Okehampton 2 St Catherines Court, 30 Devizes Road, Wroughton, Swindon
            "10026657041",  # SN15DA -> SN34HP : 25A Oxford Street, Swindon
            "200001116137",  # SN40RZ -> SN14BJ : Winchester 4 St Catherines Court, 30 Devizes Road, Wroughton, Swindon
            "200001615007",  # SN40PW -> SN11DH : 47 Station Road, Chiseldon
            "200002924788",  # SN34SF -> SN34QL : Willowbrook, 47 Highworth Road, South Marston
        ]:
            rec["accept_suggestion"] = False

        return rec
