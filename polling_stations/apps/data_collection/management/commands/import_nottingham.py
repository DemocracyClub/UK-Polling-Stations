from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E06000018"
    elections = []
    scraper_name = "wdiv-scrapers/DC-PollingStations-Nottingham"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["POLLINGDIS"],
            "name": record["POLLINGDIS"],
            "area": poly,
            "polling_station_id": record["POLLINGDIS"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        return {
            "internal_council_id": record["CONST"],
            "postcode": "",
            "address": record["NAME"] + "\n" + record["ADDRESS"],
            "location": location,
        }
