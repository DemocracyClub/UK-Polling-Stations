from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "DOV"
    elections = ["2024-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Dover"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["Polling_District"],
            "name": record["Polling_District_ID"],
            "area": poly,
            "polling_station_id": f'{record["UPRN"]}-{record["Polling_District"]}',
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        return {
            "internal_council_id": f'{record["UPRN"]}-{record["Polling_District"]}',
            "postcode": "",
            "address": f"{record['Polling_Station']},{record['Station_Address']}",
            "location": location,
        }
