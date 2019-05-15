from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000029"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/Democracy Club - Polling Stations.csv"
    )
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):

        # bug report #6
        # Holy Trinity Church Centre
        if record.stationcode in ["OB_1", "OB_2"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.151435, 51.364474, srid=4326)
            return rec

        return super().station_record_to_dict(record)
