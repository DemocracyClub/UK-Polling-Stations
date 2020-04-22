import os
from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseCsvStationsJsonDistrictsImporter


"""
Define a stub implementation of json importer
district_record_to_dict() may return None
station_record_to_dict() may return None or a list
"""


class Command(BaseCsvStationsJsonDistrictsImporter):

    srid = 4326
    council_id = "X01000000"
    districts_name = "test.geojson"
    stations_name = "test.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/special_cases"
    )

    def district_record_to_dict(self, record):

        properties = record["properties"]

        if properties["id"] == "invalid":
            return None

        return {
            "council": self.council,
            "internal_council_id": properties["id"],
            "name": properties["name"],
        }

    def station_record_to_dict(self, record):

        if record.districts == "invalid":
            return None

        location = Point(float(record.lng), float(record.lat), srid=self.get_srid())

        stations = []
        districts = record.districts.split("/")
        for district in districts:
            stations.append(
                {
                    "council": self.council,
                    "internal_council_id": district,
                    "postcode": record.postcode,
                    "address": record.address,
                    "location": location,
                    "polling_district_id": district,
                }
            )

        return stations
