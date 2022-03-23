from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SLA"
    addresses_name = (
        "2022-04-14/2022-03-23T12:30:54.401519/polling_station_export-2022-03-23.csv"
    )
    stations_name = (
        "2022-04-14/2022-03-23T12:30:54.401519/polling_station_export-2022-03-23.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "109-selside-memorial-hall":
            rec["location"] = Point(-2.709031, 54.398317, srid=4326)

        return rec

    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "LA6 2NA",
            "LA12 7JS",
            "LA23 1PE",
            "LA7 7DG",
            "LA7 7EB",
            "LA8 8LF",
            "LA9 5ES",
            "LA9 7PE",
            "LA9 7SF",
        ]:
            return None

        return super().address_record_to_dict(record)
