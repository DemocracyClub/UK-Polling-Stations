from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000012"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")
        if uprn == "38303584":
            rec["postcode"] = "L40UQ"

        # The following UPRN corrections are from local.2019-05-02 but have been checked to still be relevant.
        if uprn in [
            "38002209",  # L199DG -> L199BN : Lone Oak, Aigburth Hall Road, Liverpool
            "38287679",  # L77EZ -> L77BL : Flat 4.06 Tudor Close, Mulberry Street, Liverpool
            "38287683",  # L77EZ -> L77BL : Flat 5.12 Tudor Close, Mulberry Street, Liverpool
            "38287685",  # L77EZ -> L77BL : Flat 5.21 Tudor Close, Mulberry Street, Liverpool
            "38287691",  # L77EZ -> L77BL : Flat 6.13 Tudor Close, Mulberry Street, Liverpool
            "38287700",  # L77EZ -> L77BL : Flat 7.22 Tudor Close, Mulberry Street, Liverpool
            "38287706",  # L77EZ -> L77EE : Flat 8.21 Tudor Close, Mulberry Street, Liverpool
            "38287708",  # L77EZ -> L77EE : Flat 8.23 Tudor Close, Mulberry Street, Liverpool
            "38287717",  # L77EZ -> L77BL : Flat 10.11 Tudor Close, Mulberry Street, Liverpool
            "38287723",  # L77EZ -> L77BL : Flat 11.01 Tudor Close, Mulberry Street, Liverpool
            "38287726",  # L77EZ -> L77BL : Flat 11.13 Tudor Close, Mulberry Street, Liverpool
            "38287734",  # L77EZ -> L77EE : Flat 12.21 Tudor Close, Mulberry Street, Liverpool
            "38287740",  # L77EZ -> L77BL : Flat 13.04 Tudor Close, Mulberry Street, Liverpool
            "38287743",  # L77EZ -> L77BL : Flat 13.07 Tudor Close, Mulberry Street, Liverpool
            "38287750",  # L77EZ -> L77BL : Flat 14.06 Tudor Close, Mulberry Street, Liverpool
            "38287753",  # L77EZ -> L77BL : Flat 15.01 Tudor Close, Mulberry Street, Liverpool
            "38287759",  # L77EZ -> L77BL : Flat 15.07 Tudor Close, Mulberry Street, Liverpool
            "38287686",  # L77EZ -> L77BL : Flat 5.22 Tudor Close, Mulberry Street, Liverpool
            "38287694",  # L77EZ -> L77BL : Flat 6.23 Tudor Close, Mulberry Street, Liverpool
            "38287697",  # L77EZ -> L77BL : Flat 7.12 Tudor Close, Mulberry Street, Liverpool
            "38287702",  # L77EZ -> L77EE : Flat 8.01 Tudor Close, Mulberry Street, Liverpool
            "38287703",  # L77EZ -> L77EE : Flat 8.11 Tudor Close, Mulberry Street, Liverpool
            "38287714",  # L77EZ -> L77BL : Flat 9.22 Tudor Close, Mulberry Street, Liverpool
            "38287719",  # L77EZ -> L77BL : Flat 10.13 Tudor Close, Mulberry Street, Liverpool
            "38287720",  # L77EZ -> L77BL : Flat 10.21 Tudor Close, Mulberry Street, Liverpool
            "38287722",  # L77EZ -> L77BL : Flat 10.23 Tudor Close, Mulberry Street, Liverpool
            "38287737",  # L77EZ -> L77BL : Flat 13.01 Tudor Close, Mulberry Street, Liverpool
            "38287739",  # L77EZ -> L77BL : Flat 13.03 Tudor Close, Mulberry Street, Liverpool
            "38287745",  # L77EZ -> L77BL : Flat 14.01 Tudor Close, Mulberry Street, Liverpool
            "38287748",  # L77EZ -> L77BL : Flat 14.04 Tudor Close, Mulberry Street, Liverpool
            "38287661",  # L77EZ -> L77BL : Flat TC1.01 Tudor Close, Mulberry Street, Liverpool
            "38287675",  # L77EZ -> L77EE : Flat TC3.07 Tudor Close, Mulberry Street, Liverpool
            "38206702",  # L83SL -> L80TH : Flat 3 Grove House, Sefton Park Road, Liverpool
            "38206704",  # L83SL -> L80TH : Flat 5 Grove House, Sefton Park Road, Liverpool
            "38206705",  # L83SL -> L80TH : Flat 6 Grove House, Sefton Park Road, Liverpool
            "38237715",  # L45RQ -> L45RJ : Flat 1, 269 Walton Lane, Liverpool
            "38027340",  # L43RB -> L43QZ : Flat 2, 134 Carisbrooke Road, Liverpool
            "38268660",  # L46UF -> L46UD : 28A Walton Hall Avenue, Liverpool
            "38120389",  # L135XD -> L135XE : The Masons Arms, Prescot Road, Liverpool
            "38089048",  # L150EQ -> L153HA : 154A Lawrence Road, Liverpool
            "38006109",  # L114TD -> L110BS : Croxteth Park Care Home, Altcross Road, Liverpool
            "38039508",  # L120HA -> L120HR : Clk of Works House, Croxteth Hall Lane, Liverpool
            "38049794",  # L122AH -> L122AJ : 387A Eaton Road, Liverpool
            "38243176",  # L137BA -> L137BB : Flat 1, 87 Green Lane, Liverpool
            "38243177",  # L137BA -> L137BB : Flat 2, 87 Green Lane, Liverpool
            "38180077",  # L125HW -> L120HA : West Derby Lodge, West Derby Village, Liverpool
            "38287746",  # L77EZ -> L77BL : Flat 14.02 Tudor Close, Mulberry Street, Liverpool
            "38287678",  # L77EZ -> L77BL : Flat 4.05 Tudor Close, Mulberry Street, Liverpool
            "38299148",  # L77AJ -> L77AL : Flat C4008 Vine Court, 35 Myrtle Street, Liverpool
            "38299156",  # L77AJ -> L77AL : Flat C4016 Vine Court, 35 Myrtle Street, Liverpool
            "38299157",  # L77AJ -> L77AL : Flat C4017 Vine Court, 35 Myrtle Street, Liverpool
            "38299163",  # L77AJ -> L77AL : Flat C4023 Vine Court, 35 Myrtle Street, Liverpool
            "38299174",  # L77AJ -> L77AL : Flat C5002 Vine Court, 35 Myrtle Street, Liverpool
            "38299179",  # L77AJ -> L77AL : Flat C5007 Vine Court, 35 Myrtle Street, Liverpool
            "38299180",  # L77AJ -> L77AL : Flat C5008 Vine Court, 35 Myrtle Street, Liverpool
            "38299299",  # L77AJ -> L77AL : Flat D4015 Vine Court, 35 Myrtle Street, Liverpool
            "38299301",  # L77AJ -> L77AL : Flat D4022 Vine Court, 35 Myrtle Street, Liverpool
            "38299308",  # L77AJ -> L77AL : Flat D4041 Vine Court, 35 Myrtle Street, Liverpool
            "38299309",  # L77AJ -> L77AL : Flat D4042 Vine Court, 35 Myrtle Street, Liverpool
            "38299142",  # L77AJ -> L77AL : Flat C4002 Vine Court, 35 Myrtle Street, Liverpool
            "38299151",  # L77AJ -> L77AL : Flat C4011 Vine Court, 35 Myrtle Street, Liverpool
            "38299160",  # L77AJ -> L77AL : Flat C4020 Vine Court, 35 Myrtle Street, Liverpool
            "38299177",  # L77AJ -> L77AL : Flat C5005 Vine Court, 35 Myrtle Street, Liverpool
            "38299183",  # L77AJ -> L77AL : Flat C5011 Vine Court, 35 Myrtle Street, Liverpool
            "38299296",  # L77AJ -> L77AL : Flat D4012 Vine Court, 35 Myrtle Street, Liverpool
            "38299302",  # L77AJ -> L77AL : Flat D4031 Vine Court, 35 Myrtle Street, Liverpool
            "38299306",  # L77AJ -> L77AL : Flat D4035 Vine Court, 35 Myrtle Street, Liverpool
            "38299311",  # L77AJ -> L77AL : Flat D4044 Vine Court, 35 Myrtle Street, Liverpool
            "38299314",  # L77AJ -> L77AL : Flat D4051 Vine Court, 35 Myrtle Street, Liverpool
            "38299320",  # L77AJ -> L77AL : Flat D4073 Vine Court, 35 Myrtle Street, Liverpool
            "38317578",  # L77EZ -> L77BL : Flat 13.09 Tudor Close, Mulberry Street, Liverpool
            "38317577",  # L77EZ -> L77BL : Flat 14.09 Tudor Close, Mulberry Street, Liverpool
            "38245855",  # L78UE -> L70LA : Flat 1, 15A Prescot Street, Liverpool
            "38299303",  # L77AJ -> L77AL : Flat D4032 Vine Court, 35 Myrtle Street, Liverpool
            "38312712",  # L150EQ -> L150EP : Flat 9, 108 Lawrence Road, Liverpool
            "38287667",  # L77EZ -> L77BL : Flat TC2.02 Tudor Close, Mulberry Street, Liverpool
            "38287662",  # L77EZ -> L77BL : Flat TC1.02 Tudor Close, Mulberry Street, Liverpool
            "38287673",  # L77EZ -> L77EE : Flat TC3.05 Tudor Close, Mulberry Street, Liverpool
            "38287661",  # L77EZ -> L77BL : Flat 1.01 Tudor Close, Mulberry Street, Liverpool
            "38287667",  # L77EZ -> L77BL : Flat 2.02 Tudor Close, Mulberry Street, Liverpool
            "38287665",  # L77EZ -> L77BL : Flat 1.07 Tudor Close, Mulberry Street, Liverpool
            "38287669",  # L77EZ -> L77BL : Flat 2.06 Tudor Close, Mulberry Street, Liverpool
            "38287666",  # L77EZ -> L77BL : Flat 3.01 Tudor Close, Mulberry Street, Liverpool
            "38287670",  # L77EZ -> L77BL : Flat 3.07 Tudor Close, Mulberry Street, Liverpool
            "38147051",  # L45QY -> L209ET : 2C Stuart Road, Liverpool
            "38287688",  # L77EZ -> L77BL : Flat 6.01 Tudor Close, Mulberry Street, Liverpool
            "38287711",  # L77EZ -> L77BL : Flat 9.12 Tudor Close, Mulberry Street, Liverpool
            "38287728",  # L77EZ -> L77BL : Flat 11.22 Tudor Close, Mulberry Street, Liverpool
            "38287731",  # L77EZ -> L77EE : Flat 12.11 Tudor Close, Mulberry Street, Liverpool
            "38287756",  # L77EZ -> L77BL : Flat 15.04 Tudor Close, Mulberry Street, Liverpool
            "38287666",  # L77EZ -> L77BL : Flat TC2.01 Tudor Close, Mulberry Street, Liverpool
            "38287664",  # L77EZ -> L77BL : Flat TC1.06 Tudor Close, Mulberry Street, Liverpool
            "38287669",  # L77EZ -> L77BL : Flat TC2.06 Tudor Close, Mulberry Street, Liverpool
            "38287668",  # L77EZ -> L77BL : Flat 2.05 Tudor Close, Mulberry Street, Liverpool
            "38299145",  # L77AJ -> L77AL : Flat C4005 Vine Court, 35 Myrtle Street, Liverpool
            "38299162",  # L77AJ -> L77AL : Flat C4022 Vine Court, 35 Myrtle Street, Liverpool
            "38299165",  # L77AJ -> L77AL : Flat C4025 Vine Court, 35 Myrtle Street, Liverpool
            "38299182",  # L77AJ -> L77AL : Flat C5010 Vine Court, 35 Myrtle Street, Liverpool
            "38299317",  # L77AJ -> L77AL : Flat D4062 Vine Court, 35 Myrtle Street, Liverpool
            "38300273",  # L70EU -> L70EA : Rooms At, 13 Beech Street, Liverpool
            "38147050",  # L45QY -> L209ET : 2B Stuart Road, Liverpool
            "38287696",  # L77EZ -> L77BL : Flat 7.11 Tudor Close, Mulberry Street, Liverpool
            "38287713",  # L77EZ -> L77BL : Flat 9.21 Tudor Close, Mulberry Street, Liverpool
            "38287736",  # L77EZ -> L77EE : Flat 12.23 Tudor Close, Mulberry Street, Liverpool
            "38287755",  # L77EZ -> L77BL : Flat 15.03 Tudor Close, Mulberry Street, Liverpool
            "38287758",  # L77EZ -> L77BL : Flat 15.06 Tudor Close, Mulberry Street, Liverpool
            "38287671",  # L77EZ -> L77EE : Flat TC3.01 Tudor Close, Mulberry Street, Liverpool
            "38287669",  # L77EZ -> L77BL : Flat 3.06 Tudor Close, Mulberry Street, Liverpool
            "38299147",  # L77AJ -> L77AL : Flat C4007 Vine Court, 35 Myrtle Street, Liverpool
            "38299173",  # L77AJ -> L77AL : Flat C5001 Vine Court, 35 Myrtle Street, Liverpool
            "38299298",  # L77AJ -> L77AL : Flat D4014 Vine Court, 35 Myrtle Street, Liverpool
            "38299316",  # L77AJ -> L77AL : Flat D4061 Vine Court, 35 Myrtle Street, Liverpool
            "38299319",  # L77AJ -> L77AL : Flat D4072 Vine Court, 35 Myrtle Street, Liverpool
            "38243179",  # L137BA -> L137BB : Flat 4, 87 Green Lane, Liverpool
            "38287687",  # L77EZ -> L77BL : Flat 5.23 Tudor Close, Mulberry Street, Liverpool
            "38287704",  # L77EZ -> L77EE : Flat 8.12 Tudor Close, Mulberry Street, Liverpool
            "38287727",  # L77EZ -> L77BL : Flat 11.21 Tudor Close, Mulberry Street, Liverpool
            "38287730",  # L77EZ -> L77EE : Flat 12.01 Tudor Close, Mulberry Street, Liverpool
            "38287744",  # L77EZ -> L77BL : Flat 13.08 Tudor Close, Mulberry Street, Liverpool
            "38287749",  # L77EZ -> L77BL : Flat 14.05 Tudor Close, Mulberry Street, Liverpool
            "38287665",  # L77EZ -> L77BL : Flat TC1.07 Tudor Close, Mulberry Street, Liverpool
            "38287663",  # L77EZ -> L77BL : Flat TC1.05 Tudor Close, Mulberry Street, Liverpool
            "38287668",  # L77EZ -> L77BL : Flat TC2.05 Tudor Close, Mulberry Street, Liverpool
            "38299164",  # L77AJ -> L77AL : Flat C4024 Vine Court, 35 Myrtle Street, Liverpool
            "38299181",  # L77AJ -> L77AL : Flat C5009 Vine Court, 35 Myrtle Street, Liverpool
            "38299307",  # L77AJ -> L77AL : Flat D4036 Vine Court, 35 Myrtle Street, Liverpool
            "38299310",  # L77AJ -> L77AL : Flat D4043 Vine Court, 35 Myrtle Street, Liverpool
            "38245522",  # L192JJ -> L191QL : Flat 1, 140 St Mary`s Road, Liverpool
            "38101714",  # L125EB -> L125EA : 43 Meadow Lane, Liverpool
            "38206703",  # L83SL -> L80TH : Flat 4 Grove House, Sefton Park Road, Liverpool
            "38300727",  # L169JD -> L168NB : Apartment 2 Green Lane Annex Apartments, Taggart Avenue, Liverpool
            "38287695",  # L77EZ -> L77BL : Flat 7.01 Tudor Close, Mulberry Street, Liverpool
            "38287721",  # L77EZ -> L77BL : Flat 10.22 Tudor Close, Mulberry Street, Liverpool
            "38287738",  # L77EZ -> L77BL : Flat 13.02 Tudor Close, Mulberry Street, Liverpool
            "38287662",  # L77EZ -> L77BL : Flat 1.02 Tudor Close, Mulberry Street, Liverpool
            "38299155",  # L77AJ -> L77AL : Flat C4015 Vine Court, 35 Myrtle Street, Liverpool
            "38299300",  # L77AJ -> L77AL : Flat D4021 Vine Court, 35 Myrtle Street, Liverpool
            "38206701",  # L83SL -> L80TH : Flat 2 Grove House, Sefton Park Road, Liverpool
            "38243206",  # L133BN -> L132BN : Flat 1, 23 Greenfield Road, Liverpool
            "38147052",  # L45QY -> L209ET : 2D Stuart Road, Liverpool
            "38287689",  # L77EZ -> L77BL : Flat 6.11 Tudor Close, Mulberry Street, Liverpool
            "38287712",  # L77EZ -> L77BL : Flat 9.13 Tudor Close, Mulberry Street, Liverpool
            "38287729",  # L77EZ -> L77BL : Flat 11.23 Tudor Close, Mulberry Street, Liverpool
            "38287754",  # L77EZ -> L77BL : Flat 15.02 Tudor Close, Mulberry Street, Liverpool
            "38287757",  # L77EZ -> L77BL : Flat 15.05 Tudor Close, Mulberry Street, Liverpool
            "38287670",  # L77EZ -> L77BL : Flat TC2.07 Tudor Close, Mulberry Street, Liverpool
            "38287668",  # L77EZ -> L77BL : Flat 3.05 Tudor Close, Mulberry Street, Liverpool
            "38299146",  # L77AJ -> L77AL : Flat C4006 Vine Court, 35 Myrtle Street, Liverpool
            "38299315",  # L77AJ -> L77AL : Flat D4052 Vine Court, 35 Myrtle Street, Liverpool
            "38299318",  # L77AJ -> L77AL : Flat D4071 Vine Court, 35 Myrtle Street, Liverpool
            "38317750",  # L137DG -> L137DE : Flat 1, 117/119 Moscow Drive, Liverpool
            "38320120",  # L258RP -> L255NH : The Flat Above, 31 Woolton Street, Liverpool
            "38287682",  # L77EZ -> L77BL : Flat 5.11 Tudor Close, Mulberry Street, Liverpool
            "38287699",  # L77EZ -> L77BL : Flat 7.21 Tudor Close, Mulberry Street, Liverpool
            "38287725",  # L77EZ -> L77BL : Flat 11.12 Tudor Close, Mulberry Street, Liverpool
            "38287742",  # L77EZ -> L77BL : Flat 13.06 Tudor Close, Mulberry Street, Liverpool
            "38287677",  # L77EZ -> L77BL : Flat 4.02 Tudor Close, Mulberry Street, Liverpool
            "38287705",  # L77EZ -> L77EE : Flat 8.13 Tudor Close, Mulberry Street, Liverpool
            "38287680",  # L77EZ -> L77BL : Flat 4.07 Tudor Close, Mulberry Street, Liverpool
            "38287664",  # L77EZ -> L77BL : Flat 1.06 Tudor Close, Mulberry Street, Liverpool
            "38299153",  # L77AJ -> L77AL : Flat C4013 Vine Court, 35 Myrtle Street, Liverpool
            "38299159",  # L77AJ -> L77AL : Flat C4019 Vine Court, 35 Myrtle Street, Liverpool
            "38299176",  # L77AJ -> L77AL : Flat C5004 Vine Court, 35 Myrtle Street, Liverpool
            "38299305",  # L77AJ -> L77AL : Flat D4034 Vine Court, 35 Myrtle Street, Liverpool
            "38289089",  # L257RG -> L181LW : 74A Allerton Road, Liverpool
            "38287690",  # L77EZ -> L77BL : Flat 6.12 Tudor Close, Mulberry Street, Liverpool
            "38287693",  # L77EZ -> L77BL : Flat 6.22 Tudor Close, Mulberry Street, Liverpool
            "38287710",  # L77EZ -> L77BL : Flat 9.11 Tudor Close, Mulberry Street, Liverpool
            "38287716",  # L77EZ -> L77BL : Flat 10.01 Tudor Close, Mulberry Street, Liverpool
            "38287733",  # L77EZ -> L77EE : Flat 12.13 Tudor Close, Mulberry Street, Liverpool
            "38287680",  # L77EZ -> L77BL : Flat TC4.07 Tudor Close, Mulberry Street, Liverpool
            "38287674",  # L77EZ -> L77EE : Flat TC3.06 Tudor Close, Mulberry Street, Liverpool
            "38299150",  # L77AJ -> L77AL : Flat C4010 Vine Court, 35 Myrtle Street, Liverpool
            "38299167",  # L77AJ -> L77AL : Flat C4027 Vine Court, 35 Myrtle Street, Liverpool
            "38299295",  # L77AJ -> L77AL : Flat D4011 Vine Court, 35 Myrtle Street, Liverpool
            "38245857",  # L78UE -> L70LA : Flat 3, 15A Prescot Street, Liverpool
            "38152834",  # L40RG -> L40RQ : Park Hotel, 194 Walton Breck Road, Liverpool
            "38287684",  # L77EZ -> L77BL : Flat 5.13 Tudor Close, Mulberry Street, Liverpool
            "38287724",  # L77EZ -> L77BL : Flat 11.11 Tudor Close, Mulberry Street, Liverpool
            "38287752",  # L77EZ -> L77BL : Flat 14.08 Tudor Close, Mulberry Street, Liverpool
            "38287747",  # L77EZ -> L77BL : Flat 14.03 Tudor Close, Mulberry Street, Liverpool
            "38287670",  # L77EZ -> L77BL : Flat 2.07 Tudor Close, Mulberry Street, Liverpool
            "38299141",  # L77AJ -> L77AL : Flat C4001 Vine Court, 35 Myrtle Street, Liverpool
            "38299144",  # L77AJ -> L77AL : Flat C4004 Vine Court, 35 Myrtle Street, Liverpool
            "38299158",  # L77AJ -> L77AL : Flat C4018 Vine Court, 35 Myrtle Street, Liverpool
            "38299161",  # L77AJ -> L77AL : Flat C4021 Vine Court, 35 Myrtle Street, Liverpool
            "38299184",  # L77AJ -> L77AL : Flat C5012 Vine Court, 35 Myrtle Street, Liverpool
            "38299313",  # L77AJ -> L77AL : Flat D4046 Vine Court, 35 Myrtle Street, Liverpool
            "38066021",  # L137EA -> L137EB : Churchview Nursing Home, Green Lane, Liverpool
            "38155977",  # L257RX -> L257RW : Gardeners Arms, Vale Road, Liverpool
            "38206700",  # L83SL -> L80TH : Flat 1 Grove House, Sefton Park Road, Liverpool
            "38037227",  # L43QN -> L43QW : 110A County Road, Liverpool
            "38287681",  # L77EZ -> L77BL : Flat 5.01 Tudor Close, Mulberry Street, Liverpool
            "38287698",  # L77EZ -> L77BL : Flat 7.13 Tudor Close, Mulberry Street, Liverpool
            "38287701",  # L77EZ -> L77BL : Flat 7.23 Tudor Close, Mulberry Street, Liverpool
            "38287718",  # L77EZ -> L77BL : Flat 10.12 Tudor Close, Mulberry Street, Liverpool
            "38287741",  # L77EZ -> L77BL : Flat 13.05 Tudor Close, Mulberry Street, Liverpool
            "38287760",  # L77EZ -> L77BL : Flat 15.08 Tudor Close, Mulberry Street, Liverpool
            "38317579",  # L77EZ -> L77BL : Flat 15.09 Tudor Close, Mulberry Street, Liverpool
            "38287707",  # L77EZ -> L77EE : Flat 8.22 Tudor Close, Mulberry Street, Liverpool
            "38287676",  # L77EZ -> L77BL : Flat 4.01 Tudor Close, Mulberry Street, Liverpool
            "38287663",  # L77EZ -> L77BL : Flat 1.05 Tudor Close, Mulberry Street, Liverpool
            "38287666",  # L77EZ -> L77BL : Flat 2.01 Tudor Close, Mulberry Street, Liverpool
            "38299152",  # L77AJ -> L77AL : Flat C4012 Vine Court, 35 Myrtle Street, Liverpool
            "38299175",  # L77AJ -> L77AL : Flat C5003 Vine Court, 35 Myrtle Street, Liverpool
            "38299178",  # L77AJ -> L77AL : Flat C5006 Vine Court, 35 Myrtle Street, Liverpool
            "38299304",  # L77AJ -> L77AL : Flat D4033 Vine Court, 35 Myrtle Street, Liverpool
            "38243178",  # L137BA -> L137BB : Flat 3, 87 Green Lane, Liverpool
            "38147049",  # L45QY -> L209ET : 2A Stuart Road, Liverpool
            "38287692",  # L77EZ -> L77BL : Flat 6.21 Tudor Close, Mulberry Street, Liverpool
            "38287709",  # L77EZ -> L77BL : Flat 9.01 Tudor Close, Mulberry Street, Liverpool
            "38287715",  # L77EZ -> L77BL : Flat 9.23 Tudor Close, Mulberry Street, Liverpool
            "38287732",  # L77EZ -> L77EE : Flat 12.12 Tudor Close, Mulberry Street, Liverpool
            "38287735",  # L77EZ -> L77EE : Flat 12.22 Tudor Close, Mulberry Street, Liverpool
            "38287751",  # L77EZ -> L77BL : Flat 14.07 Tudor Close, Mulberry Street, Liverpool
            "38287676",  # L77EZ -> L77BL : Flat TC4.01 Tudor Close, Mulberry Street, Liverpool
            "38287672",  # L77EZ -> L77EE : Flat TC3.02 Tudor Close, Mulberry Street, Liverpool
            "38287667",  # L77EZ -> L77BL : Flat 3.02 Tudor Close, Mulberry Street, Liverpool
            "38299143",  # L77AJ -> L77AL : Flat C4003 Vine Court, 35 Myrtle Street, Liverpool
            "38299149",  # L77AJ -> L77AL : Flat C4009 Vine Court, 35 Myrtle Street, Liverpool
            "38299166",  # L77AJ -> L77AL : Flat C4026 Vine Court, 35 Myrtle Street, Liverpool
            "38299297",  # L77AJ -> L77AL : Flat D4013 Vine Court, 35 Myrtle Street, Liverpool
            "38299312",  # L77AJ -> L77AL : Flat D4045 Vine Court, 35 Myrtle Street, Liverpool
            "38168495",  # L168NA -> L168NB : 265 Woolton Road, Liverpool
            "38245856",  # L78UE -> L70LA : Flat 2, 15A Prescot Street, Liverpool
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "38291517",  # L133BS -> L142DD : Rooms At, 325 Prescot Road, Liverpool
            "38248655",
            "38326441",
            "38289089",
            "38312647",
            "38252912",
            "38252915",
            "38252918",
            "38252917",
            "38252911",
            "38252914",
            "38252913",
            "38252916",
            "38312954",
            "38307125",
            "38307126",
            "38307127",
            "38307128",
            "38307129",
            "38245855",
            "38245856",
            "38245857",
            "38321863",
            "38321864",
            "38321865",
            "38321866",
            "38282429",
            "38282430",
            "38325987",
            "38325988",
            "38268559",
            "38268560",
            "38268561",
            "38268562",
            "38300977",
            "38300978",
            "38300979",
            "38300980",
            "38300981",
            "38300982",
            "38243654",
            "38238875",
            "38238876",
            "38238877",
            "38314085",
            "38237230",
            "38241124",
            "38237648",
            "38237649",
            "38245835",
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6.strip() in ["L25 7RA"]:
            return None

        return rec
