from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "E06000014"
    elections = ["local.2019-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-York"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["CODE"],
            "name": "%s - %s" % (record["WARD"], record["CODE"]),
            "area": poly,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = record["POLLINGDIS"].split(" / ")
        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code.strip(),
                    "postcode": "",
                    "address": record["POLLINGSTA"],
                    "location": location,
                    "polling_district_id": code.strip(),
                }
            )
        return stations
