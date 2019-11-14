from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000127"
    addresses_name = (
        "parl.2019-12-12/Version 1/West lancashire Democracy_Club__12December2019.TSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/West lancashire Democracy_Club__12December2019.TSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10012355528":
            return None

        if record.addressline6.strip() == "L33 3AL":
            return None

        if record.addressline6.strip() in (
            "PR8 5JE",
            "PR4 6SA",
            "L39 8TR",
            "L40 6JP",
            "PR4 6XA",
        ):
            # One or more properties has a wrong-looking polling station, so play it safe
            return None

        if record.addressline6.strip() == "PR9 8DF":
            # Riverside Caravan Park, which has lots of suggested postcode fixes. Traditionally we have said no to
            # these
            rec["accept_suggestion"] = False

        if uprn in [
            "10012347931",  # L408HQ -> L408HR : Quarry Barn, Pinfold Lane, Scarisbrick, Ormskirk
            "100012818795",  # WN69PS -> WN69QB : 9 Highmoor, Whittle Lane, Wrightington, Wigan
            "100012414932",  # L399EE -> L399EG : Boundary Farm, Graveyard Lane, Bickerstaffe, Ormskirk
            "10012341232",  # L401UH -> L401UA : Ivy Cottage, Holmeswood Road, Holmeswood, Ormskirk
            "100012417385",  # WN86SH -> WN87SH : Tildesley Farmhouse, Elmers Green Lane, Skelmersdale
            "100012657720",  # L408JB -> L408JR : Langley Brook Farm, Langley Road, Burscough, Ormskirk
            "100010675945",  # WN88EN -> WN88PU : 83 School Lane, Skelmersdale
            "200001130134",  # WN87XA -> WN87XF : Crossing Cottage, Ferrett Lane, Lathom, Ormskirk
            "200002847950",  # L398RL -> L398BB : Meadowbank Barn, Halsall Lane, Halsall, Ormskirk
        ]:
            rec["accept_suggestion"] = True
        #
        if uprn in [
            "100010684796",  # WN80AA -> WN80AB : 168 Ormskirk Road, Up Holland, Skelmersdale
            "100010684616",  # WN80AG -> WN80AH : 11 Ormskirk Road, Up Holland, Skelmersdale
            "100010684618",  # WN80AG -> WN80AH : 13 Ormskirk Road, Up Holland, Skelmersdale
            "100010684620",  # WN80AG -> WN80AH : 15 Ormskirk Road, Up Holland, Skelmersdale
            "100010684622",  # WN80AG -> WN80AH : 17 Ormskirk Road, Up Holland, Skelmersdale
            "100010684609",  # WN80AG -> WN80AH : 3 Ormskirk Road, Up Holland, Skelmersdale
            "100010684611",  # WN80AG -> WN80AH : 5 Ormskirk Road, Up Holland, Skelmersdale
            "100010684612",  # WN80AG -> WN80AH : 7 Ormskirk Road, Up Holland, Skelmersdale
            "100012654494",  # L397HS -> L397HQ : Rose Croft, Broad Lane, Downholland, Ormskirk
            "100012821133",  # WN88AU -> WN80PB : 21 Liverpool Road, Skelmersdale
            "100012657542",  # L407SN -> L407SL : The Homestead Merridale Farm, High Lane, Ormskirk
            "100012415199",  # L407SN -> L407SL : The Mount, High Lane, Ormskirk
            "10012356919",  # WN80HS -> WN89QS : 93 Dearden Way, Up Holland, Skelmersdale
            "10012344656",  # L406JA -> L406JT : Ottershead Barn, Dicks Lane, Lathom, Ormskirk
            "100012414799",  # L406JA -> L406JT : Whitestone Cottage, Dicks Lane, Lathom, Ormskirk
            "100012418034",  # WN69EN -> WN69EQ : Glen View, Hall Lane, Wrightington, Wigan
            "100010677297",  # WN80EW -> WN80EN : Hallbridge Farmhouse, 59 Dingle Road, Up Holland, Skelmersdale
            "100010682656",  # WN80QY -> WN80QZ : Pearsons Farm, Lafford Lane, Up Holland, Skelmersdale
            "100012657092",  # L405SW -> L405UZ : Lyme House, Junction Lane, Burscough, Ormskirk
            "10012357601",  # L393BH -> L393BW : 14 Park Road, Ormskirk
            # Wrong postcode in AddressBase
            "100012416134",  # L390HF -> L390HP : The Flat Quattros, Rainford Road, Bickerstaffe, Ormskirk
            "10012363368",  # WN89HU -> WN89BH : 1 Beechtrees Mews, Beechtrees, Skelmersdale
            "10012363370",  # WN89HU -> WN89BH : 3 Beechtrees Mews, Beechtrees, Skelmersdale
            "10012363372",  # WN89HU -> WN89BH : 5 Beechtrees Mews, Beechtrees, Skelmersdale
            "10012363374",  # WN89HU -> WN89BH : 7 Beechtrees Mews, Beechtrees, Skelmersdale
            "10012363376",  # WN89HU -> WN89BH : 9 Beechtrees Mews, Beechtrees, Skelmersdale
            "10012363378",  # WN89HU -> WN89BH : 11 Beechtrees Mews, Beechtrees, Skelmersdale
        ]:
            rec["accept_suggestion"] = False

        return rec
