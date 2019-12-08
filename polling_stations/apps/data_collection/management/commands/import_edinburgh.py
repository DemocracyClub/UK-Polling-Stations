import tempfile
import urllib.request
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "S12000036"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Edinburgh"
    geom_type = "geojson"

    def get_stations(self):
        with tempfile.NamedTemporaryFile() as tmp:
            urllib.request.urlretrieve(self.stations_url, tmp.name)
            stations = self.get_data(self.stations_filetype, tmp.name)
            # ad-hoc fixes for parl.2019-12-12
            stations.append(
                {
                    "Polling__1": "Assembly Rooms",
                    "Address_1": "54 George Street",
                    "geometry": '{ "type": "Feature", "geometry": null }',
                    "LG_PP": "NC11A",
                }
            )
            stations.append(
                {
                    "Polling__1": "Dalmeny Parish Church Hall",
                    "Address_1": "Main Street",
                    "geometry": '{ "type": "Feature", "geometry": null }',
                    "LG_PP": "WW01C",
                }
            )
            return stations

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["Code2016"],
            "name": record["NEWWARD"] + " - " + record["Code2016"],
            "area": poly,
            "polling_station_id": record["Code2016"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = record["LG_PP"].split("/")
        codes = [code.strip() for code in codes]

        stations = []
        for code in codes:
            station = {
                "internal_council_id": code,
                "address": "\n".join([record["Polling__1"], record["Address_1"]]),
                "postcode": "",
                "location": location,
            }
            stations.append(station)

        return stations
