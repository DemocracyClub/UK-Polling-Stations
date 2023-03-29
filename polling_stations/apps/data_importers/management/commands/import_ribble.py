from django.contrib.gis.geos import Point

from data_importers.base_importers import BaseStationsDistrictsImporter


class Command(BaseStationsDistrictsImporter):
    srid = 27700
    council_id = "RIB"
    elections = ["2023-05-04"]
    districts_name = "2023-05-04/2023-03-29T13:51:45/PD.geojson"
    stations_name = "2023-05-04/2023-03-29T13:51:45/PS.geojson"
    stations_filetype = "geojson"
    districts_filetype = "geojson"

    def station_record_to_dict(self, record):
        stations = []
        codes = (
            c.strip()
            for c in (
                record["properties"]["CODE"],
                record["properties"]["CODE 2"],
                record["properties"]["CODE 3"],
            )
            if c
        )
        name = record["properties"]["Name"].strip()
        address = record["properties"]["Address"].strip()
        postcode = record["properties"]["Postcode"].strip()
        location = Point(
            record["properties"]["longitude"],
            record["properties"]["latitude"],
            srid=4326,
        )
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code,
                    "address": f"{name}\n{address}",
                    "postcode": postcode,
                    "polling_district_id": code,
                    "location": location,
                }
            )
        return stations

    def district_record_to_dict(self, record):
        return {
            "internal_council_id": record["properties"]["CODE"].strip(),
            "name": record["properties"]["NAME"],
        }
