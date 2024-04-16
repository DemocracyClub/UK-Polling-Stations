from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    council_id = "SEV"
    elections = ["2024-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Sevenoaks"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["AreaCode"],
            "name": "%s - %s" % (record["Name"], record["AreaCode"]),
            "area": poly,
            "polling_station_id": record["AreaCode"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        return {
            "internal_council_id": record["AreaCode"],
            "postcode": "",
            "address": record["Address"],
            "location": location,
        }
