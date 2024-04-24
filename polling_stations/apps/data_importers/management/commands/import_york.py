import re

from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "YOR"
    elections = ["2024-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-York"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        code = record["Code"].replace("/", "")
        return {
            "internal_council_id": code,
            "name": "%s - %s" % (record["Ward"], record["Code"]),
            "area": poly,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = re.split("[, ]", record["PollingDistrict"])
        codes = [code.strip() for code in codes if code.strip()]
        # codes = [code.strip() for code in record["PollingDistrict"].split("/")]
        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code.strip(),
                    "postcode": "",
                    "address": f'{record["PlaceName"]}/{record["Address"]}',
                    "location": location,
                    "polling_district_id": code.strip(),
                }
            )
        return stations
