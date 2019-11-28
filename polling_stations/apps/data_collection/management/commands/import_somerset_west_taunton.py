from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000246"
    addresses_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019somersetw.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019somersetw.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Williams Hall
        if rec["internal_council_id"] == "8079":
            rec["location"] = Point(-2.930949, 51.041262, srid=4326)

        # Victoria Park Pavilion
        if rec["internal_council_id"] == "8219":
            rec["location"] = Point(-3.091719, 51.017816, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in [
            "TA4 1CQ",
            "TA22 9JH",
            "TA24 8NS",
            "TA23 0HL",
        ]:
            return None

        if uprn == "10003766208":
            rec["postcode"] = "TA22 9AD"

        if uprn == "10023838852":
            rec["postcode"] = "TA5 1TW"

        if uprn in [
            "200003159967",  # TA247UF -> TA247TQ : 1 Slades Cottage, Great House Street
            "10023837182",  # TA43PX -> TA43PU : Sadies Lodge, Elworthy Lydeard St Lawrence
            "10003560944",  # TA245BG -> TA246BG : Flat 2 5 The Terrace, Bircham Road, Alcombe, Minehead, Somerset
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
