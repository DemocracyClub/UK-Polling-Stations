from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2023-05-04/2023-03-16T13:16:16.307677/Eros_SQL_Output005.csv"
    stations_name = "2023-05-04/2023-03-16T13:16:16.307677/Eros_SQL_Output005.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "CB4 2QA",
            "CB4 1LD",
            # wrong
            "CB1 7UF",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "43-the-c3-centre":
            rec["location"] = Point(0.1572, 52.2003, srid=4326)

        # user issue report #105
        if rec["internal_council_id"] == "32-trinity-old-field-pavilion":
            rec["location"] = Point(0.106029, 52.207284, srid=4326)

        # user issue report #129
        if rec["internal_council_id"] == "3-east-barnwell-community-centre":
            rec["location"] = Point(0.165576, 52.212132, srid=4326)

        # report from council
        if rec["internal_council_id"] == "13-seminar-rooms-3-4":
            rec["location"] = Point(0.099002518, 52.215464, srid=4326)

        return rec
