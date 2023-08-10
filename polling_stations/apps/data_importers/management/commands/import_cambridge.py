from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2023-07-04/2023-05-31T14:59:32.696409/Eros_SQL_Output013.csv"
    stations_name = "2023-07-04/2023-05-31T14:59:32.696409/Eros_SQL_Output013.csv"
    elections = ["2023-07-04"]
    easting_field = "pollingstationeasting"
    northing_field = "pollingstationnorthing"

    def get_station_point(self, record):
        if (
            hasattr(record, self.easting_field)
            and hasattr(record, self.northing_field)
            and getattr(record, self.easting_field) != "0"
            and getattr(record, self.easting_field) != ""
            and getattr(record, self.northing_field) != "0"
            and getattr(record, self.northing_field) != ""
        ):
            # if we've got points, use them

            return Point(
                float(getattr(record, self.easting_field)),
                float(getattr(record, self.northing_field)),
                srid=27700,
            )

        return super().get_station_point(record)
