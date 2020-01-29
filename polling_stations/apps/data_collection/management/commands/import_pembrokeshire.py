from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "W06000009"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Pembrokeshire"
    geom_type = "geojson"
    seen_stations = set()

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["DistrictRef"],
            "name": record["DistrictName"],
            "area": poly,
        }

    def station_record_to_dict(self, record):
        if record["County"] == "Carmarthenshire":
            return None

        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = record["DistricttRef"].split(";")
        stations = []
        for code in codes:
            if code not in self.seen_stations:
                self.seen_stations.add(code)
                stations.append(
                    {
                        "internal_council_id": code,
                        "postcode": "",
                        "address": record["StationName"],
                        "location": location,
                        "polling_district_id": code,
                    }
                )
            else:
                print(f"Discarding duplicate station for code {code}")

        return stations
