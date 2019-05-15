from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000178"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019ox.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019ox.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "200004681758":
            rec["postcode"] = "OX2 6TQ"

        if uprn == "10093785403":
            rec["postcode"] = "OX4 4RS"

        if uprn == "10091102017":
            rec["postcode"] = "OX3 0SN"

        if uprn == "10013991465":

            rec["postcode"] = "OX4 2NH"

        if uprn == "10024243546":
            rec["postcode"] = "OX4 3DQ"

        if uprn in ["10091102003", "10091102004", "10091102005"]:
            rec["postcode"] = "OX4 3QD"

        if uprn == "100120827844":
            return None

        if uprn == "10024245588":
            return None

        return rec

    def station_record_to_dict(self, record):

        # Baptist Church Room, Godstow Road, Wolvercote
        if record.polling_place_id == "4904":
            record = record._replace(polling_place_postcode="OX2 8PG")

        # Aspire, Former St Thomas School, Osney Lane
        if record.polling_place_id == "5124":
            record = record._replace(polling_place_postcode="OX1 1NJ")

        # St Margaret`s Centre Hall, 30 Polstead Road
        if record.polling_place_id == "4929":
            record = record._replace(polling_place_postcode="OX2 6TN")

        # Littlemore Community Centre, Giles Road
        if record.polling_place_id == "5116":
            record = record._replace(polling_place_postcode="OX4 4NW")

        rec = super().station_record_to_dict(record)
        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] == "4995":
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        return rec
