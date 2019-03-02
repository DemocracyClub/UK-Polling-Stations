from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000246"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019somersetW.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019somersetW.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "6954":
            record = record._replace(polling_place_postcode="TA4 2JP")

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
