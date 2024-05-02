from data_importers.management.commands import BaseDemocracyCountsCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = (
        "2024-05-02/2024-03-25T13:12:33.651843/DC Clubs_PollingDistricts_CAMDEN.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-25T13:12:33.651843/DC Clubs_PollingStations_CAMDEN.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # bug report # 649:
        # moving point closer to road for: GOSPEL OAK METHODIST CHURCH, Agincourt Road, London
        rec = super().station_record_to_dict(record)
        if rec["internal_council_id"] in (
            "IA-b",
            "IA-a",
        ):
            rec["location"] = Point(527726, 185479, srid=27700)

        return rec
