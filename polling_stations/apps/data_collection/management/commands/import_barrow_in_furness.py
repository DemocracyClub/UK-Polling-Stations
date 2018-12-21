from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E07000027"
    elections = ["parl.2017-06-08"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-BarrowInFurness"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["INFO"],
            "name": record["INFO"],
            "area": poly,
            "polling_station_id": record["INFO"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        return {
            "internal_council_id": record["POLLING_DISTRICT"],
            "postcode": "",
            "address": "%s\n%s"
            % (record["POLLING_STATION"], record["POLLING_ADDRESS"]),
            "location": location,
        }
