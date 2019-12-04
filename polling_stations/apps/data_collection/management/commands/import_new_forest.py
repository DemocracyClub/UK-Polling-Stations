from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000091"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019nf.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019nf.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # correction: https://trello.com/c/R5XolnQC
        if record.polling_place_id == "7903":  # New Milton Cricket Club
            record = record._replace(polling_place_postcode="BH25 5SU")

        # user issue report #195
        if record.polling_place_id == "7942":  # Sandleheath Village Hall
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.817931, 50.931645, srid=4326)
            return rec

        # corrections from council
        if record.polling_place_id == "7953":  # Woodgreen Village Hall
            record = record._replace(polling_place_easting="417079.23")
            record = record._replace(polling_place_northing="117684.73")
        if record.polling_place_id == "7836":  # Fordingbridge Town Hall
            record = record._replace(polling_place_easting="414713.35")
            record = record._replace(polling_place_northing="114134.91")
        if record.polling_place_id == "7784":  # Totton & Eling Cricket Club
            record = record._replace(polling_place_easting="435321.7")
            record = record._replace(polling_place_northing="113089.68")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10007461147", "100062214501"]:
            return None

        return rec
