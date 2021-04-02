from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "WLV"
    elections = ["2021-05-06"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Wolverhampton"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["DIS_CODE_NEW"],
            "name": record["WARD"] + " - " + record["DIS_CODE_NEW"],
            "area": poly,
            "polling_station_id": record["DIS_CODE_NEW"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = record["DIS_CODE_NEW"].split(",")
        codes = [code.strip() for code in codes]

        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code,
                    "address": record["ADDRESS"],
                    "postcode": record["POSTCODE"],
                    "location": location,
                }
            )
        return stations
