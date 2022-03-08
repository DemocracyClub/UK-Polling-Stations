from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STN"
    addresses_name = "2022-05-05/2022-03-08T12:51:22.118970/Democracy Club Data Polling Districts.csv"
    stations_name = (
        "2022-05-05/2022-03-08T12:51:22.118970/Democracy Club Data Polling Stations.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        # bug report #6
        # Holy Trinity Church Centre
        if record.stationcode in ["RB/1", "RB/2"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.151435, 51.364474, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode == "SM6 9BY":
            return None

        return super().address_record_to_dict(record)
