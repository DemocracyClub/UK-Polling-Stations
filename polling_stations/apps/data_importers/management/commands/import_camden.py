from data_importers.management.commands import BaseDemocracyCountsCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = "2026-05-07/2026-03-09T12:26:15.372546/Democracy Club - Polling Districts_CAMDEN.csv"
    stations_name = "2026-05-07/2026-03-09T12:26:15.372546/Democracy Club - Polling Stations_CAMDEN.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "5193668",  # 21 MILL LANE, LONDON
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "NW6 5UA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # moving point closer to road for: GOSPEL OAK METHODIST CHURCH, Agincourt Road, London
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] in (
            "IA/1",
            "IA/2",
        ):
            rec["location"] = Point(527726, 185479, srid=27700)

        # correct point for: ABBEY COMMUNITY CENTRE 172 Belsize Road London
        if rec["internal_council_id"] == "FB":
            rec["location"] = Point(525888, 183945, srid=27700)

        # fix data for 2 stations under same address:
        # N1C CENTRE, Plimsoll Building, 1 Handyside Street, London, NIC 4BQ
        if rec["internal_council_id"] in ("PD", "PC"):
            rec["postcode"] = "N1C 4BQ"
            rec["location"] = Point(529972, 183722, srid=27700)

        return rec
