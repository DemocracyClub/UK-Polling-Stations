from data_importers.geo_utils import fix_bad_polygons
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    council_id = "AGB"
    elections = ["2022-05-05"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Wolverhampton"
    geom_type = "geojson"
    srid = 4326
    districts_srid = 4326

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["CODE"],
            "name": record["NAME"] + " - " + record["CODE"],
            "area": poly,
            "polling_station_id": record["CODE"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = record["CODE"].split(",")
        codes = [code.strip() for code in codes]

        stations = []
        for code in codes:
            station = {
                "internal_council_id": code,
                "address": record["ADDRESS"],
                "postcode": "",
                "location": location,
            }
            if code == "AA19":
                station["name"] = "Islay Customer Service Point"
                station["address"] = "Jamieson Street, Bowmore, Isle of Islay, PA43 7HP"
                station["location"] = None
            stations.append(station)
        return stations

    def post_import(self):
        fix_bad_polygons()
