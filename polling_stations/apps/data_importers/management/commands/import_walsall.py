from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WLL"
    addresses_name = "2021-02-04T16:32:23.115281/polling_station_export-2021-02-04.csv"
    stations_name = "2021-02-04T16:32:23.115281/polling_station_export-2021-02-04.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090903309",  # FLAT 2 74 STAFFORD STREET, WILLENHALL
            "10090903310",  # Flat 1, 73 STAFFORD STREET, WALSALL
            "100071550039",  # LIVING AREA 5 JOHN STREET, WALSALL
        ]:
            return None
        if record.housepostcode in [
            "WS3 2DX",
            "WS3 3XA",
            "WV12 4BZ",
            "WV12 4BZ",
            "WS1 3LD",
            "WS4 1GB",
            "WS4 1GA",
            "WV12 5QA",
            "WS10 7TG",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # 66-st-michaels-church
        if record.pollingstationnumber == "66":
            rec["location"] = Point(-1.971183, 52.625281, srid=4326)

        return rec
