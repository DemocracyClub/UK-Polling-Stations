from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000127"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019WL.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019WL.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10012355528":
            return None

        if record.addressline6.strip() == "L33 3AL":
            return None

        if uprn in [
            "10012347931",  # L408HQ -> L408HR : Quarry Barn, Pinfold Lane, Scarisbrick, Ormskirk
            "100012818795",  # WN69PS -> WN69QB : 9 Highmoor, Whittle Lane, Wrightington, Wigan
            "100012414932",  # L399EE -> L399EG : Boundary Farm, Graveyard Lane, Bickerstaffe, Ormskirk
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10012356166",  # PR98DF -> PR98EW : 6 The Pines, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012352093",  # PR98DF -> PR98DW : 12 Wild Rose, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012357596",  # PR98DF -> PR98DW : 4 Wild Rose, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012355753",  # PR98DF -> PR98DW : 2 Wild Rose, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012358320",  # PR98DF -> PR98DW : 9 Wild Rose, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012358345",  # PR98DF -> PR98DW : 7 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012358760",  # PR98DF -> PR98DJ : 5 Hazelwood Close, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012360416",  # PR98DF -> PR98DW : 14 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012358970",  # PR98DF -> PR98DW : 11 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012359010",  # PR98DF -> PR98DJ : 14 Rosemary Avenue, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012360430",  # PR98DF -> PR98DW : Jelly Bean Lodge 1 Maple Drive, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361355",  # PR98DF -> PR98DW : 3 Hazelwood Close, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361410",  # PR98DF -> PR98DW : 32 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361429",  # PR98DF -> PR98DW : 26 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012357456",  # PR98DF -> PR98RY : Pitch 111 Riverside Caravan Park, Southport New Road, Banks, Southport
            "10012361513",  # PR98DF -> PR98DW : 2 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361514",  # PR98DF -> PR98DW : 3 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361515",  # PR98DF -> PR98DW : 4 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361516",  # PR98DF -> PR98DW : 5 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361517",  # PR98DF -> PR98DW : 6 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361519",  # PR98DF -> PR98DW : 8 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361520",  # PR98DF -> PR98DW : 9 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361521",  # PR98DF -> PR98DW : 10 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361522",  # PR98DF -> PR98DW : 11 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361523",  # PR98DF -> PR98DW : 12 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361524",  # PR98DF -> PR98DW : 13 Sycamore Court, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361874",  # PR98DF -> PR98DW : 20 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361960",  # PR98DF -> PR98DW : 17 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012361998",  # PR98DF -> PR98DW : 25 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012362471",  # PR98DF -> PR98DW : 24 Hunters Walk, Riverside Caravan Park - Southport New Road, Tarleton, Preston
            "10012363301",  # PR98DF -> PR98EW : 2 Cedar Close, Riverside Caravan Park - Southport New Road, Tarleton, Preston
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
            "10012363326",  # L392EJ -> L392DE : 1000 Walmsley Drive, Ormskirk
            "100010675944",  # WN88PU -> WN88EN : 83B School Lane, Skelmersdale
            "100012657542",  # L407SN -> L407SL : The Homestead Merridale Farm, High Lane, Ormskirk
            "100012415199",  # L407SN -> L407SL : The Mount, High Lane, Ormskirk
            "10012341150",  # L407SN -> L407GA : 6 Blythe Meadow, High Lane, Ormskirk
            "10012341151",  # L407SN -> L407GA : 7 Blythe Meadow, High Lane, Ormskirk
            "10012356919",  # WN80HS -> WN89QS : 93 Dearden Way, Up Holland, Skelmersdale
            "10012344656",  # L406JA -> L406JT : Ottershead Barn, Dicks Lane, Lathom, Ormskirk
            "100012414799",  # L406JA -> L406JT : Whitestone Cottage, Dicks Lane, Lathom, Ormskirk
            "100012418034",  # WN69EN -> WN69EQ : Glen View, Hall Lane, Wrightington, Wigan
            "100010677297",  # WN80EW -> WN80EN : Hallbridge Farmhouse, 59 Dingle Road, Up Holland, Skelmersdale
            "100010682656",  # WN80QY -> WN80QZ : Pearsons Farm, Lafford Lane, Up Holland, Skelmersdale
            "100010667268",  # L397EA -> L394QW : 245 St Helens Road, Lathom Skelmersdale
        ]:
            rec["accept_suggestion"] = False

        return rec
