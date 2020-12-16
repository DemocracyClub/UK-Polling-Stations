from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "E07000123"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Preston"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["polling_district_ref"],
            "name": "%s - %s" % (record["ward_name"], record["polling_district_ref"]),
            "area": poly,
            "polling_station_id": record["polling_station_ref"],
        }

    def format_address(self, record):
        return "\n".join(
            [record["polling_station_name"], record["polling_station_address"]]
        ).strip()

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        return {
            "internal_council_id": record["polling_station_ref"],
            "address": self.format_address(record),
            "postcode": "",
            "location": location,
        }
