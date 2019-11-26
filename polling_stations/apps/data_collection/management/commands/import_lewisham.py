from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000023"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019lewis.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019lewis.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Sir Francis Drake Primary School
        if record.polling_place_id == "16834":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.041453, 51.485092, srid=4326)
            return rec

        # All Saints Community Centre
        if record.polling_place_id == "16883":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.048807, 51.476468, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023229356",
            "100022011071",
            "100021989292",
            "200000554179",
            "100022009747",
            "100021935766",
            "100021935767",
            "100022010695",
            "100021978708",
            "10023226416",
            "10023226417",
            "100021990762",
        ]:
            return None

        if record.addressline6 in ["SE14 5NP", "SE14 5UH"]:
            return None

        return rec
