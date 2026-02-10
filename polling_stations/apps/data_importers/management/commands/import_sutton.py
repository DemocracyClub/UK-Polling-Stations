from data_importers.management.commands import BaseDemocracyCountsCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STN"
    addresses_name = (
        "2026-05-07/2026-02-10T16:13:59.794024/Modern Democracy Export PDs.csv"
    )
    stations_name = "2026-05-07/2026-02-10T16:13:59.794024/Modern Democracy Export.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # more accurate point for: Holy Trinity Church Centre, Maldon Road, Wallington, SM6 8BL
        if record.stationcode in ["RB/1", "RB/2"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.151435, 51.364474, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "5870080008",  # 4 BELMONT ROAD, WALLINGTON
        ]:
            return None

        return super().address_record_to_dict(record)
