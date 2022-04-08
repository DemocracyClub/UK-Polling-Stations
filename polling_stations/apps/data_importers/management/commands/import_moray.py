from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    council_id = "MRY"
    elections = ["2022-05-05"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Moray"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["PD_CODE"],
            "name": record["PD_NAME"],
            "area": poly,
            "polling_station_id": record["PD_CODE"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        return {
            "internal_council_id": record["PD_CODE"],
            "address": record["Addr"],
            "postcode": "",
            "location": location,
        }
