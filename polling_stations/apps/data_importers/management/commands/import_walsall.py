from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WLL"
    addresses_name = (
        "2022-05-05/2022-03-04T14:26:29.368353/polling_station_export-2022-03-03.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-04T14:26:29.368353/polling_station_export-2022-03-03.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093460948",  # CASTLEHILL SPECIALIST CARE HOME, 390 CHESTER ROAD, WALSALL
            "100071550039",  # LIVING AREA 5 JOHN STREET, WALSALL
            "100071072854",  # 59 NEW STREET, SHELFIELD, WALSALL
            "100071072810",  # 9A NEW STREET, SHELFIELD, WALSALL
            "10090902979",  # 235 STAFFORD STREET, WALSALL
            "10090903310",  # FLAT 1 73 STAFFORD STREET, WILLENHALL
            "10013665979",  # FLATS 2 AND 4 32 LYSWAYS STREET, WALSALL
            "200002877500",  # 43A HIGH STREET, BROWNHILLS, WALSALL
        ]:
            return None

        if record.housepostcode in [
            "WS1 3LD",
            "WS2 7LU",
            "WS3 1FJ",
            "WS3 2DX",
            "WS3 5AE",
            "WS4 1GA",
            "WV12 4BZ",
            "WV12 5QA",
            "WV12 5YH",
            "WS10 7TG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)

        # ST. MICHAELS CHURCH HALL HALL LANE PELSALL WALSALL
        if record.pollingstationnumber == "66":
            rec["location"] = Point(-1.971183, 52.625281, srid=4326)

        return rec
