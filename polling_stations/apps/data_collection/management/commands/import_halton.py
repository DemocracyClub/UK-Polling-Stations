from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000006"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "298":
            record = record._replace(polling_place_postcode="WA7 5DJ")

        if record.polling_place_id == "268":
            record = record._replace(polling_place_postcode="WA8 4PU")

        if record.polling_place_id == "320":
            record = record._replace(polling_place_postcode="WA7 2FL")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.701970, 53.320739, srid=4326)
            return rec

        if record.polling_place_id == "388":
            record = record._replace(polling_place_postcode="WA7 6JW")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "WA8 8SF":
            return None

        if uprn in ["10010612061", "10010612062", "10010612064"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "WA7 6HG"
            return rec

        return super().address_record_to_dict(record)
