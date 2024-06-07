from data_importers.management.commands import BaseDemocracyCountsCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STN"
    addresses_name = (
        "2024-07-04/2024-06-07T20:21:55.085664/Democracy Club Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-07T20:21:55.085664/Democracy Club Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # more accurate point for: Holy Trinity Church Centre, Maldon Road, Wallington, SM6 8BL
        if record.stationcode in ["RB/1", "RB/2"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.151435, 51.364474, srid=4326)
            return rec

        return super().station_record_to_dict(record)
