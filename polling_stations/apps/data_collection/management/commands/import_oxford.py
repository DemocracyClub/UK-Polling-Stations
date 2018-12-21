from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000178"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Oxford.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Oxford.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] == "4699":
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        return rec

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10013991465":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "OX4 2NH"
            return rec

        if uprn == "10024243546":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "OX4 3DQ"
            return rec

        if uprn in ["10091102003", "10091102004", "10091102005"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "OX4 3QD"
            return rec

        if uprn == "100120827844":
            return None

        if uprn == "10024245588":
            return None

        return super().address_record_to_dict(record)
