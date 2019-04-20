from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000005"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Rochdale.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Rochdale.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Mobile Unit at Black Dog Pub
        if record.polling_place_id == "2829":
            record = record._replace(polling_place_postcode="OL12 7JG")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.186986, 53.631252, srid=4326)
            return rec

        # Bowls Pavilion
        if record.polling_place_id == "2577":
            record = record._replace(polling_place_postcode="")

        # The Coach House
        if record.polling_place_id == "2469":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.0961003, 53.6444469, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "23033168":
            rec["postcode"] = "OL10 4NS"

        if uprn == "23025164":
            rec["postcode"] = "M24 2SD"

        if record.addressline6.strip() == "OL15 OHX":
            rec["postcode"] = "OL15 0HX"

        if uprn == "23037819":
            rec["postcode"] = "OL11 5HR"

        if uprn == "23081457":
            rec["postcode"] = "OL12 9AA"

        if record.addressline6.strip() == "OL16 3BX":
            return None

        if record.addressline6.strip() == "M24 5TG":
            return None

        if uprn == "23099282":
            rec["postcode"] = "OL11 3AU"

        if record.addressline6.strip() == "OL16 5SJ":
            return None

        if record.addressline6.strip() == "M24 2YS":
            return None

        if uprn in ["23095362", "23095226"]:
            rec["postcode"] = "OL12 9NE"

        return rec
