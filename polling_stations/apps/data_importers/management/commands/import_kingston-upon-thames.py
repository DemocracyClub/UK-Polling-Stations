from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "KTT"
    elections = ["2021-05-06"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Kingston"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["CODE"],
            "name": record["CODE"],
            "area": poly,
            "polling_station_id": record["CODE"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        return {
            "internal_council_id": record["CODE"],
            "address": record["ADDRESS"],
            "postcode": "",
            "location": location,
        }
