from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WLL"
    addresses_name = (
        "2021-03-30T11:27:49.115128/Walsall New polling_station_export-2021-03-29.csv"
    )
    stations_name = (
        "2021-03-30T11:27:49.115128/Walsall New polling_station_export-2021-03-29.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090065721",  # 279 HIGH STREET, BROWNHILLS, WALSALL
            "200002877500",  # 43A HIGH STREET, BROWNHILLS, WALSALL
            "10093460948",  # CASTLEHILL SPECIALIST CARE HOME, 390 CHESTER ROAD, WALSALL
            "100071550039",  # LIVING AREA 5 JOHN STREET, WALSALL
            "100071072854",  # 59 NEW STREET, SHELFIELD, WALSALL
            "100071072810",  # 9A NEW STREET, SHELFIELD, WALSALL
            "10013665979",  # FLATS 2 AND 4 32 LYSWAYS STREET, WALSALL
            "10090903152",  # REAR OF 26, CALDMORE GREEN, WALSALL
            "10090902979",  # 235 STAFFORD STREET, WALSALL
            "10013665316",  # YMCA, PREMSONS HOUSE, GREEN LANE, WALSALL
            "200003317397",  # CHRIST CHURCH RECTORY, BLAKENALL HEATH, WALSALL
            "10090903310",  # FLAT 1 73 STAFFORD STREET, WILLENHALL
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
            "WV12 5YH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)

        # ST. MICHAELS CHURCH HALL HALL LANE PELSALL WALSALL
        if record.pollingstationnumber == "66":
            rec["location"] = Point(-1.971183, 52.625281, srid=4326)

        return rec
