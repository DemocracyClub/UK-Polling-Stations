from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "E09000013"
    elections = []
    scraper_name = "wdiv-scrapers/DC-PollingStations-HammersmithAndFulham"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["POLLING_ZO"],
            "name": record["POLLING_ZO"],
            "area": poly,
            "polling_station_id": record["POLLING_ZO"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        return {
            "internal_council_id": record["POLLING_DI"],
            "address": record["POLLING__1"],
            "postcode": record["POSTCODE"],
            "location": location,
        }
