import json
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.collections import MultiPolygon, Polygon
from data_importers.geo_utils import fix_bad_polygons
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 27700
    districts_srid = 27700
    council_id = "SAL"
    elections = ["2021-05-06"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-StAlbans"
    geom_type = "geojson"

    def extract_poly_from_geometrycollection(self, geo_collection):
        for feature in geo_collection:
            if isinstance(feature, Polygon):
                return self.clean_poly(
                    GEOSGeometry(feature.wkt, srid=self.get_srid("districts"))
                )

    def extract_json_geometry(self, record, srid):
        geom = json.loads(record["geometry"])

        # delete any junk which will cause us to throw
        # Invalid number of points in LinearRing found 3 - must be 0 or >= 4
        if geom["geometry"]["type"] == "MultiPolygon":
            for i, poly in enumerate(geom["geometry"]["coordinates"]):
                if len(poly[0]) < 4:
                    del geom["geometry"]["coordinates"][i]

        geojson = json.dumps(geom["geometry"])
        poly = self.clean_poly(GEOSGeometry(geojson))
        poly.srid = srid
        return poly

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        if isinstance(poly, MultiPolygon):
            area = poly
        else:
            area = self.extract_poly_from_geometrycollection(poly)

        return {
            "internal_council_id": record["DISTRICT"],
            "name": record["WARD"] + " - " + record["DISTRICT"],
            "area": area,
            "polling_station_id": record["DISTRICT"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        return {
            "internal_council_id": record["PD"],
            "address": record["LOCATION"],
            "postcode": "",
            "location": location,
        }

    def post_import(self):
        fix_bad_polygons()
