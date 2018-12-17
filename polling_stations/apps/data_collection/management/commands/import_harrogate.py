from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000165"
    addresses_name = "local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "10513":
            record = record._replace(polling_place_postcode="HG4 5ET")

        if record.polling_place_id == "10374":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.845862, 54.156945, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100052009106":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "HG3 5AT"
            return rec

        return super().address_record_to_dict(record)
