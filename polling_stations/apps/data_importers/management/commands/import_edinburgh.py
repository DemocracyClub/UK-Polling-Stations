from data_importers.geo_utils import fix_bad_polygons
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "EDH"
    elections = ["2021-05-06"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Edinburgh"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        if record["Code2016"] == "EE11K":
            record["Code2016"] = "EN11K"

        return {
            "internal_council_id": record["Code2016"],
            "name": record["NEWWARD"] + " - " + record["Code2016"],
            "area": poly,
            "polling_station_id": record["Code2016"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = record["LG_PP"].split("/")
        codes = [code.strip() for code in codes]

        stations = []
        for code in codes:
            # Slateford Longstone Parish Church Hall
            if code == "SWP07N":
                location = None
            station = {
                "internal_council_id": code,
                "address": "\n".join([record["Polling__1"], record["Address_1"]]),
                "postcode": "",
                "location": location,
            }
            stations.append(station)

        return stations

    def post_import(self):
        fix_bad_polygons()
