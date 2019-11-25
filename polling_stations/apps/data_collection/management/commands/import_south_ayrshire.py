import tempfile
import urllib.request
from data_collection.github_importer import BaseGitHubImporter
from data_collection.slugger import Slugger


"""
This one is a bit messy.

The districts file has station addresses in it

There is also a stations file with points, but it has no codes
so we're going to parse the districts file twice
(once for the shapes and once to fill in the station addresses)
and then we'll fill in the points from the stations file
using address slug where possible.
"""


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "S12000028"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-SouthAyrshire"
    geom_type = "geojson"
    stations_query = "districts"
    station_points = {}

    def pre_import(self):
        filename = self.base_url % (self.council_id, "stations", "json")
        with tempfile.NamedTemporaryFile() as tmp:
            urllib.request.urlretrieve(filename, tmp.name)
            stations = self.get_data("json", tmp.name)
            for station in stations:
                self.station_points[Slugger.slugify(station["place"])] = station

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["polling"],
            "name": record["polling"],
            "area": poly,
            "polling_station_id": record["polling"],
        }

    def station_record_to_dict(self, record):
        if not record["place"]:
            return None

        slug = Slugger.slugify(record["place"])
        if slug in self.station_points:
            location = self.extract_geometry(
                self.station_points[slug], self.geom_type, self.get_srid()
            )
        else:
            location = None

        return {
            "internal_council_id": record["polling"],
            "address": record["place"],
            "postcode": record["postcode"],
            "location": location,
        }
