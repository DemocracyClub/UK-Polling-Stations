from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STN"
    addresses_name = "2021-03-10T16:04:41.774562/Democracy Club Polling Districts.csv"
    stations_name = "2021-03-10T16:04:41.774562/Democracy Club Polling Stations.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):

        # bug report #6
        # Holy Trinity Church Centre
        if record.stationcode in ["OB_1", "OB_2"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.151435, 51.364474, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode == "SM6 9BY":
            return None

        return super().address_record_to_dict(record)
