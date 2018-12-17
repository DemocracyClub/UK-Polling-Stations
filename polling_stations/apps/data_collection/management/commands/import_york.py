from data_collection.morph_importer import BaseMorphApiImporter


class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E06000014"
    elections = ["parl.2017-06-08"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-York"
    geom_type = "geojson"
    split_districts = set()

    def pre_import(self):
        self.find_split_districts()

    def find_split_districts(self):
        "Identify districts mapped to more than one polling station."
        stations = self.get_stations()
        for station1 in stations:
            for station2 in stations:
                if (
                    station1["POLLINGDIS"] == station2["POLLINGDIS"]
                    and station1["pk"] != station2["pk"]
                ):
                    self.split_districts.add(station1["POLLINGDIS"])

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["CODE"],
            "name": "%s - %s" % (record["WARD"], record["CODE"]),
            "area": poly,
        }

    def station_record_to_dict(self, record):

        # Handle split districts
        if record["POLLINGDIS"] in self.split_districts:
            return None

        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        internal_ids = record["POLLINGDIS"].split(" ")
        if len(internal_ids) == 1:
            return {
                "internal_council_id": record["POLLINGDIS"],
                "postcode": "",
                "address": record["POLLINGSTA"],
                "location": location,
                "polling_district_id": record["POLLINGDIS"],
            }
        else:
            stations = []
            for id in internal_ids:
                stations.append(
                    {
                        "internal_council_id": id,
                        "postcode": "",
                        "address": record["POLLINGSTA"],
                        "location": location,
                        "polling_district_id": id,
                    }
                )
            return stations
