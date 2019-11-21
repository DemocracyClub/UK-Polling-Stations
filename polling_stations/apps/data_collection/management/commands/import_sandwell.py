from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000028"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019sand.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019sand.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "17094":
            # Hallam Street Methodist Church
            record = record._replace(polling_place_postcode="B71 4HG")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.post_code == "DY4 OQX":
            rec["postcode"] = "DY40QX"
        if record.post_code == "B7O 9LG":
            rec["postcode"] = "B709LG"
        if record.post_code == "DY4 ONT":
            rec["postcode"] = "DY40NT"
        if record.post_code == "DY4 OET":
            rec["postcode"] = "DY40ET"
        if record.post_code == "B70 OSH":
            rec["postcode"] = "B700SH"
        if record.post_code == "B68 OLH":
            rec["postcode"] = "B680LH"

        if (record.addressline1, record.addressline2, record.addressline3) == (
            "13",
            "West House",
            "Lombard Street",
        ):
            # duplicate of 13 West House, Lombard Street West, with wrong polling station
            # see https://github.com/DemocracyClub/UK-Polling-Stations/pull/2377#issuecomment-557613973
            return None

        if uprn in [
            "32145963",  # B664DH -> B664ES : Hotel Dinara, 344 Bearwood Road, Smethwick
            "100071578415",  # B664BW -> B664DP : Flat Over, 622 Bearwood Road, Smethwick
            "32125898",  # B675DQ -> B675JN : 81 St. Mary`s Road, Smethwick
            "32070225",  # B709EW -> B709ET : Fox And Goose, 161 Greets Green Road, West Bromwich
            "100071380615",  # B707HR -> B707HL : 119 Bromford Lane, West Bromwich
            "32171745",  # B421NN -> B421NT : 1A Old Walsall Road, Great Barr, Birmingham
            "100070915237",  # DY49NB -> DY49NA : Flat 1, 72 Upper Church Lane, Tipton
            "100070886589",  # B664PB -> B664RN : Flat 1, 90 Cape Hill, Smethwick
            "10008753081",  # B664DP -> B664BL : Flat Above, 609 Bearwood Road, Smethwick
            "32126253",  # B677EP -> B677EL : Ash Lodge Nursing Home, Londonderry Lane, Smethwick
            "32178576",  # DY47PF -> DY47PG : St Martins Manor, Lower Church Lane, Tipton
            "10008754069",  # B663PJ -> B663PB : 434A High Street, Smethwick
            "32040852",  # DY47PE -> DY47PG : The Court House, Lower Church Lane, Tipton
            "32143008",  # B664DP -> B664BX : Flat B, 530 Bearwood Road, Smethwick
            "10008753162",  # WS109HE -> WS109EN : Flat Over, 84-85 Walsall Street, Wednesbury
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "32049182",  # B650NE -> B650ES : Flat 1, 170/174 Halesowen Street, Rowley Regis
            "32049183",  # B650NE -> B650ES : Flat 2, 170/174 Halesowen Street, Rowley Regis
            "32115462",  # B711AE -> B688JA : 149 Vicarage Road, West Bromwich
            "10090607805",  # WS109AX -> B700NG : 32A Wood Green Road, Wednesbury
            "200001912478",  # B706HG -> B650BB : Flat 2, 101 Beeches Road, West Bromwich
            "32109442",  # B650EH -> B706NZ : 55 High Street, Rowley Regis
        ]:
            rec["accept_suggestion"] = False

        return rec
