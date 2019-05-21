from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000246"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019somersetW.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019somersetW.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        """
        These changes are from local.2019-05-02 to europarl.2019-05-23 from Somerset and West Taunton Council
        Duplicate stations are being created to retain granularity of control wrt to polling districts.
        """

        # · Cheddon Fitzpaine Memorial Hall -> West Monkton Village Hall (already a polling station)
        if record.polling_place_id == "6924":
            record = record._replace(
                polling_place_name="Cheddon Fitzpaine Memorial Hall"
            )
            record = record._replace(polling_place_address_1="Rowford")
            record = record._replace(polling_place_address_2="Cheddon Fitzpaine")
            record = record._replace(polling_place_address_4="Taunton")
            record = record._replace(polling_place_postcode="TA2 8JY")

        # · Crowcombe Church House -> Crowcombe Hall, Crowcombe TA4 4AQ
        if record.polling_place_id == "6830":
            record = record._replace(polling_place_name="Crowcombe Hall")
            record = record._replace(polling_place_address_1="Crowcombe")
            record = record._replace(polling_place_postcode="TA4 4AQ")

        # · St James Church, St James Street, Taunton -> Victoria Park Pavilion (already a polling station)
        if record.polling_place_id == "6866":
            record = record._replace(polling_place_name="Victoria Park Pavilion")
            record = record._replace(polling_place_address_1="Victoria Gate")
            record = record._replace(polling_place_address_4="Taunton")
            record = record._replace(polling_place_postcode="TA1 3ES")

        # · The Function Room at The Beambridge Inn, Sampford Arundel -> Parish Room, Sampford Arundel (already a polling station)
        if record.polling_place_id == "6715":
            record = record._replace(polling_place_name="The Parish Room")
            record = record._replace(polling_place_address_1="Sampford Arundel")
            record = record._replace(polling_place_address_2="Wellington")
            record = record._replace(polling_place_postcode="")

        # · The 68 Club, Cheddon Road, Taunton -> The Meeting Room, Wellsprings Leisure Centre (already a polling station)
        if record.polling_place_id == "6800":
            record = record._replace(polling_place_name="Meeting Room")
            record = record._replace(
                polling_place_address_1="Wellsprings Leisure Centre"
            )
            record = record._replace(polling_place_address_2="Cheddon Road")
            record = record._replace(polling_place_address_4="Taunton")
            record = record._replace(polling_place_postcode="TA2 7QP")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["TA4 1GQ", "TA4 1CQ"]:
            return None

        if uprn == "10003766208":
            rec["postcode"] = "TA22 9AD"

        if uprn == "10023838852":
            rec["postcode"] = "TA5 1TW"

        if uprn in [
            "200003159967",  # TA247UF -> TA247TQ : 1 Slades Cottage, Great House Street
            "10023837182",  # TA43PX -> TA43PU : Sadies Lodge, Elworthy Lydeard St Lawrence
            "10003560944",  # TA245BG -> TA246BG : Flat 2 5 The Terrace, Bircham Road, Alcombe, Minehead, Somerset
            "100040944958",  # TA14YH -> TA14PZ : 1A Bruford Close, Taunton, Somerset
            "100040944959",  # TA14YH -> TA14PZ : 1B Bruford Close, Taunton, Somerset
            "100040944961",  # TA14YH -> TA14PZ : 2B Bruford Close, Taunton, Somerset
            "100040944964",  # TA14YH -> TA14PZ : 4A Bruford Close, Taunton, Somerset
            "100040944966",  # TA14YH -> TA14PZ : 5A Bruford Close, Taunton, Somerset
            "100040944972",  # TA14YH -> TA14PZ : 8A Bruford Close, Taunton, Somerset
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100040951701",  # TA218AQ -> TA218AG : 28 Fore Street, Wellington, Somerset
            "10008798212",  # TA43EX -> TA43EZ : The Old Granary, 2 Sevenash Cottages, Seven Ash
            "10008798255",  # TA43PU -> TA43RX : Knights Farm, Lydeard St Lawrence
        ]:
            rec["accept_suggestion"] = False

        if uprn == "10008799187":
            rec["postcode"] = "TA3 5AE"

        return rec
