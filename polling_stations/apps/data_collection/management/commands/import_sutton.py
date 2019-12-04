from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000029"
    addresses_name = (
        "parl.2019-12-12/Version 1/Polling Districts Sutton 12 December 2019.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Polling Stations Sutton 12 December 2019.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # bug report #6
        # Holy Trinity Church Centre
        if record.stationcode in ["OB_1", "OB_2"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.151435, 51.364474, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "5870041842":
            return None

        return rec
