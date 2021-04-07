from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2021-03-23T09:23:18.089254/polling_station_export-2021-03-22.csv"
    stations_name = "2021-03-23T09:23:18.089254/polling_station_export-2021-03-22.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "48-the-c3-centre":
            rec["location"] = Point(0.1572, 52.2003, srid=4326)

        # user issue report #105
        if rec["internal_council_id"] == "36-trinity-old-field-pavilion":
            rec["location"] = Point(0.106029, 52.207284, srid=4326)

        # user issue report #129
        if rec["internal_council_id"] == "2-east-barnwell-community-centre":
            rec["location"] = Point(0.165576, 52.212132, srid=4326)

        # report from council
        if (
            rec["internal_council_id"] == "16-seminar-rooms-3-4-churchill-college"
            or rec["internal_council_id"] == "15-seminar-rooms-3-4-churchill-college"
        ):
            rec["location"] = Point(0.099002518, 52.215464, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090968296",  # FLAT 3, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968298",  # FLAT 5, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968295",  # FLAT 2, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968294",  # FLAT 1, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968297",  # FLAT 4, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "200004186734",  # STATION LODGE, BARNWELL JUNCTION, NEWMARKET ROAD, CAMBRIDGE
            "200004210208",  # STATION HOUSE, BARNWELL JUNCTION, NEWMARKET ROAD, CAMBRIDGE
        ]:
            return None

        if record.housepostcode in ["CB4 2QA", "CB4 1LD"]:
            return None

        return super().address_record_to_dict(record)
