from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000031"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-14.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-14.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10003949214",
            "100110697617",
            "10034113464",
        ]:
            return None

        if record.housepostcode in [
            "LA6 2NA",
            "LA23 3LX",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "109-selside-memorial-hall":
            rec["location"] = Point(-2.709031, 54.398317, srid=4326)

        return rec
