from django.contrib.gis.geos import Point, GEOSGeometry

from data_importers.base_importers import BaseCsvStationsKmlDistrictsImporter
from data_importers.management.commands import BaseCsvStationsJsonDistrictsImporter


class BaseStubCsvStationsJsonDistrictsImporter(BaseCsvStationsJsonDistrictsImporter):

    council_id = "X01000000"

    def district_record_to_dict(self, record):
        properties = record["properties"]
        return {
            "council": self.council,
            "internal_council_id": properties["id"],
            "name": properties["name"],
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.lng), float(record.lat), srid=self.get_srid())
        return {
            "council": self.council,
            "internal_council_id": record.internal_council_id,
            "postcode": record.postcode,
            "address": record.address,
            "location": location,
        }


class BaseStubCsvStationsKmlDistrictsImporter(BaseCsvStationsKmlDistrictsImporter):

    council_id = "X01000000"

    def district_record_to_dict(self, record):
        geojson = record.geom.geojson
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid("districts")))
        return {
            "internal_council_id": record["Name"].value,
            "name": record["Name"].value,
            "area": poly,
        }
