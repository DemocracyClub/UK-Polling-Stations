from data_collection.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "W06000012"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-11aber.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-11aber.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.pollingstationname == "St. Joseph's R.C Church Hall":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.800506, 51.6536899, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.housepostcode in ["SA11 3QE", "SA12 8EP", "SA9 2SA"]:
            return None

        return rec
