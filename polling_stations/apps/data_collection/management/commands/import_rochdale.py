from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000005"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Bowls Pavilion - Postcode gives wrong geocode
        if record.polling_place_id == "3132":
            record = record._replace(polling_place_postcode="")

        # The Coach House
        if record.polling_place_id == "3348":
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

        if uprn == "23099282":
            rec["postcode"] = "OL11 3AU"

        if uprn in ["23095362", "23095226"]:
            rec["postcode"] = "OL12 9NE"

        # Not quite right, safer to throw away
        if record.addressline6.strip() in [
            "OL16 3BX",
            "OL16 5SJ",
            "M24 2YS",
            "M24 5TG",
            "M24 5TN",
        ] or uprn in [
            "10023363964",
            "23108014",
            "10090922210",
            "10090922501",
            "10090922502",
            "10023364069",
            "10023364206",
        ]:
            return None

        return rec
