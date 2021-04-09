from django.contrib.gis.geos import MultiPoint
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "DOV"
    elections = ["2021-05-06"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Dover"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        code = record["district"].split("-")[0].strip()

        return {
            "internal_council_id": code,
            "name": record["district"],
            "area": poly,
            "polling_station_id": code,
        }

    def station_record_to_dict(self, record):
        if record["POLLING_DI"] == "PSHN":
            return None
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        if isinstance(location, MultiPoint) and len(location) == 1:
            location = location[0]

        address = "\n".join([record["NAME_OF_PO"], record["LOCATION"]])
        codes = record["POLLING_DI"].split("&")
        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code.strip(),
                    "postcode": record["POSTCODE"],
                    "address": address,
                    "location": location,
                }
            )
        return stations
