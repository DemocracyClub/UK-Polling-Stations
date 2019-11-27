from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E07000115"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-TonbridgeMalling"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["PROPOSED_P"],
            "name": record["PROPOSED_1"],
            "area": poly,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        address = record["ADDRESS"]

        return {
            "internal_council_id": record["OBJECTID_1"],
            "address": address,
            "postcode": "",
            "location": location,
            "polling_district_id": record["PD_LETTER"],
        }
