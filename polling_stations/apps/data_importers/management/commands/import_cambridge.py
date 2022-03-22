from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = (
        "2022-05-05/2022-03-22T14:45:23.854113/polling_station_export-2022-03-22.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-22T14:45:23.854113/polling_station_export-2022-03-22.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "47-the-c3-centre":
            rec["location"] = Point(0.1572, 52.2003, srid=4326)

        # user issue report #105
        if rec["internal_council_id"] == "35-trinity-old-field-pavilion":
            rec["location"] = Point(0.106029, 52.207284, srid=4326)

        # user issue report #129
        if rec["internal_council_id"] == "2-east-barnwell-community-centre":
            rec["location"] = Point(0.165576, 52.212132, srid=4326)

        # report from council
        if (
            rec["internal_council_id"] == "14-seminar-rooms-3-4-churchill-college"
            or rec["internal_council_id"] == "15-seminar-rooms-3-4-churchill-college"
        ):
            rec["location"] = Point(0.099002518, 52.215464, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        if record.housepostcode in ["CB4 2QA", "CB4 1LD"]:
            return None

        return super().address_record_to_dict(record)
