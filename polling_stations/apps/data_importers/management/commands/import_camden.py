from data_importers.management.commands import BaseDemocracyCountsCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = "2026-10-08/2026-09-21T12:02:48.533067/Polling Districts.csv"
    stations_name = "2026-10-08/2026-09-21T12:02:48.533067/Polling Stations.csv"
    elections = ["2026-10-08"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # fix data for 2 stations under same address:
        # N1C CENTRE, Plimsoll Building, 1 Handyside Street, London, NIC 4BQ
        if rec["internal_council_id"] in ("PD", "PC"):
            rec["postcode"] = "N1C 4BQ"
            rec["location"] = Point(529972, 183722, srid=27700)

        return rec
