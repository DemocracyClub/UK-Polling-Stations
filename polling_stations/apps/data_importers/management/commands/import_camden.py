from data_importers.management.commands import BaseDemocracyCountsCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = "2024-07-04/2024-06-19T16:20:32.968135/DemocracyClub_PollingDistricts_CAMDEN.csv"
    stations_name = (
        "2024-07-04/2024-06-19T16:20:32.968135/DemocracyClub_PollingStations_CAMDEN.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "5196036",  # 21A WEST HAMPSTEAD MEWS, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # remove stations from HRY council
        if record.stationcode in (
            "HGH-A",
            "HGH-B",
            "HGH-C",
            "HGH-Da",
            "HGH-Db",
        ):
            return None

        # bug report # 649:
        # moving point closer to road for: GOSPEL OAK METHODIST CHURCH, Agincourt Road, London
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] in (
            "IA - b",
            "IA - a",
        ):
            rec["location"] = Point(527726, 185479, srid=27700)

        # removes wrong point for: ABBEY COMMUNITY CENTRE 172 Belsize Road London
        if rec["internal_council_id"] == "FB":
            rec["location"] = None

        return rec
