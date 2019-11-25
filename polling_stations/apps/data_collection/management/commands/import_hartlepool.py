from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000001"
    addresses_name = "parl.2019-12-12/Version 3/Democracy_Club__12December 2019.TSV"
    stations_name = "parl.2019-12-12/Version 3/Democracy_Club__12December 2019.TSV"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if record.polling_place_id == "8878":

            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.191945, 54.664709, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # corrections
        if record.addressline6 in [
            "TS25 5DF",
            "TS25 2HE",
        ]:
            return None

        if uprn in ["100110020815", "100110009750", "10090070990", "100110020667"]:
            return None

        if uprn in ["10090068484", "10009734034", "100110786034"]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100110673453",
        ]:
            rec["accept_suggestion"] = False

        return rec
