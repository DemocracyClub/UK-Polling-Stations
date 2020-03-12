from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000142"
    addresses_name = "2020-02-24T14:10:21.901124/Democracy_Club__07May2020.tsv"
    stations_name = "2020-02-24T14:10:21.901124/Democracy_Club__07May2020.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["LN1 2ZN", "LN1 2TN", "LN1 2ZW"]:
            return None
        if uprn in [
            "10090699957",
            "10090700085",
        ]:
            return None

        if uprn in [
            "10013811263",  # LN22UH -> LN12UH : 3 Dellbrook Cottage, Chapel Walk, Scothern, Lincoln
        ]:
            rec["accept_suggestion"] = False
        if uprn in [
            "10013817658",  # DN211HL -> DN212HL : 36 Marshall`s Rise, Gainsborough
            "10034700987",  # LN83UB -> LN83HZ : The Close, Gallamore Lane, Middle Rasen
            "10013816676",  # LN76HX -> LN76BF : Private Accommodation Nettleton Lodge Inn, Moortown Road, Nettleton, Market Rasen
            "10034688319",  # LN83YN -> LN83PR : Highfield Farm, Moor Road#1, Owersby Moor, Market Rasen
            "100030973581",  # LN83AA -> LN82AA : The Manor, Mill Lane, Normanby-By-Spital, Market Rasen
            "10013809959",  # DN214UU -> DN214UX : Riverside Lodge, Snitterby Carr, Snitterby, Gainsborough
            "10034697916",  # DN213PF -> DN213PD : Welwyn, Kirton Road, Blyton, Gainsborough
            "10034692303",  # LN23PD -> LN23PA : Mill Farm Cottage West, Hackthorn Road, Hackthorn, Lincoln
            "10034700306",  # LN76NU -> LN76NJ : Wold Garth, Caistor Road, Nettleton, Market Rasen
            "10013814417",  # LN76HX -> LN76BF : Nettleton Lodge Game Farm, North Kelsey Road, Caistor
            "10013809954",  # DN214UU -> DN214UX : Poplar Lodge, Snitterby Carr, Gainsborough'
            "100030962667",  # LN12RD -> LN12RE : Green Acres New Farm, Fen Road, Burton, Lincoln
            "10090697760",  # LN83UL -> LN83XH : Honeybee Barns, Risby Grange, Tealby Road, Walesby, Market Rasen
            "10034691891",  # LN12EH -> LN12EL : Triangle Bungalow, Torksey Lock, Lincoln
            "100030956000",  # DN213DU -> DN213DS : Ravensfleet Farm, Ravensfleet Road, Wildsworth, Gainsborough
        ]:
            rec["accept_suggestion"] = True

        return rec
