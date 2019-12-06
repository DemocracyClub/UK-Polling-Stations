from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000178"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019ox.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019ox.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "200004681758":
            rec["postcode"] = "OX2 6TQ"

        if uprn == "10091102017":
            rec["postcode"] = "OX3 0SN"

        if uprn == "10013991465":
            rec["postcode"] = "OX4 2NH"

        if uprn == "10024243546":
            rec["postcode"] = "OX4 3DQ"

        if uprn in ["10091102003", "10091102004", "10091102005"]:
            rec["postcode"] = "OX4 3QD"

        if uprn in ["100120827844", "10024245588", "10091102602"]:
            return None

        if uprn in [
            # Addressbase issues - TODO: report to OS
            "10002762177",
            "200004684018",
            "200004684017",
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        # Baptist Church Room, Godstow Road, Wolvercote
        if record.polling_place_id == "5315":
            record = record._replace(polling_place_postcode="OX2 8PG")

        # Aspire, Former St Thomas School, Osney Lane
        if record.polling_place_id == "5314":
            record = record._replace(polling_place_postcode="OX1 1NJ")

        # Littlemore Community Centre, Giles Road
        if record.polling_place_id == "5295":
            record = record._replace(polling_place_postcode="OX4 4NW")

        rec = super().station_record_to_dict(record)
        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] == "5174":
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        # Oxford Centre for Mission Studies
        if rec["internal_council_id"] == "5344":
            rec["location"] = Point(-1.264263, 51.764185, srid=4326)

        return rec
