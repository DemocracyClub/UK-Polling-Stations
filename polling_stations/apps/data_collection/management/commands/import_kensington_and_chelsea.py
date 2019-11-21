from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000020"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019ken.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019ken.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # St Columba's Church
        if record.polling_place_id == "847":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.163128, 51.496844, srid=4326)
            return rec

        # St Cuthbert`s Centre
        if record.polling_place_id == "871":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.200082, 51.491363, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "217130227":
            return None

        if record.addressline1 == "The Studio":
            return None

        if uprn == "217126141":
            rec["postcode"] = "SW5 9EZ"
        if uprn == "217108045":
            rec["postcode"] = "W8 5DH"

        if record.addressline6.strip() == "SW1X 8HN":
            rec["postcode"] = "SW1X 8HJ"

        if (
            record.addressline6 == "W11 4LY"
            and record.addressline1 == "2B Drayson Mews"
        ):
            rec["postcode"] = "W8 4LY"

        return rec
