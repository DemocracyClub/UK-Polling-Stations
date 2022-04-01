from data_importers.geo_utils import fix_bad_polygons
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    council_id = "EDH"
    elections = ["2022-05-05"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Edinburgh"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

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

        station = {
            "internal_council_id": record["System_Ide"],
            "address": "\n".join(
                [record[field] for field in ["Address_Li", "Address__1", "Address__2"]]
            ),
            "postcode": record["Post_Code"],
            "location": location,
        }

        return station

    def post_import(self):
        fix_bad_polygons()
