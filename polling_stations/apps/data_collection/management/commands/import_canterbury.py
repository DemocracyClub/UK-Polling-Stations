from django.contrib.gis.geos import Point, MultiPoint
from data_collection.data_types import StationSet
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E07000106"
    elections = ["local.2019-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Canterbury"
    geom_type = "geojson"

    # Canterbury embed the station addresses in the districts file
    # The stations endpoint only serves up the geo data
    # (it doesn't include the station addresses)
    station_addresses = {}

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        code = record["ID"].strip()
        address = record["POLLING_PL"].strip()

        if code in self.station_addresses and self.station_addresses[code] != address:
            raise ValueError(
                "District code appears twice with 2 different station addresses"
            )

        self.station_addresses[code] = address

        return {
            "internal_council_id": code,
            "name": record["NAME"].strip() + " - " + code,
            "area": poly,
            "polling_station_id": code,
        }

    def station_record_to_dict(self, record):
        code = record["Polling_di"].strip()
        address = self.station_addresses[code]
        del self.station_addresses[code]  # remove station addresses as we use them

        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        if isinstance(location, MultiPoint) and len(location) == 1:
            location = location[0]

        # point supplied is bang on the building
        # but causes google directions API to give us a strange route
        if code == "CWE2" and address.startswith("St Dunstan"):
            location = Point(1.070064, 51.283614, srid=4326)

        return {
            "internal_council_id": code,
            "postcode": "",
            "address": address,
            "location": location,
        }

    def post_import(self):
        # mop up any districts where we have a station address
        # attached to a district code but no point
        self.stations = StationSet()
        for code in self.station_addresses:
            self.add_polling_station(
                {
                    "internal_council_id": code,
                    "postcode": "",
                    "address": self.station_addresses[code],
                    "location": None,
                    "council": self.council,
                }
            )
        self.stations.save()
