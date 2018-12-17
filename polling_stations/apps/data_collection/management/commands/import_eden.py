from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E07000030"
    elections = ["parl.2017-06-08"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Eden"
    geom_type = "geojson"
    split_districts = set()

    def pre_import(self):
        self.find_split_districts()

    def find_split_districts(self):
        "Identify districts mapped to more than one polling station."
        stations = self.get_stations()
        for station1 in stations:
            station1Codes = [
                i.strip() for i in station1["Codes"].split("/")[-1].split(",")
            ]
            for station2 in stations:
                station2Codes = [
                    i.strip() for i in station2["Codes"].split("/")[-1].split(",")
                ]
                for station1Code in station1Codes:
                    if (
                        station1Code in station2Codes
                        and station1["pk"] != station2["pk"]
                    ):
                        self.split_districts.add(station1Code)

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["Pollingdis"],
            "name": "%s - %s" % (record["Parish"], record["Pollingdis"]),
            "area": poly,
        }

    def station_record_to_dict(self, record):

        internal_ids = [i.strip() for i in record["Codes"].split("/")[-1].split(",")]

        # Handle split districts
        for id in internal_ids:
            if id in self.split_districts:
                return None

        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        if len(internal_ids) == 1:
            return {
                "internal_council_id": internal_ids[0],
                "postcode": "",
                "address": record["PollingStation"],
                "location": location,
                "polling_district_id": internal_ids[0],
            }
        else:
            stations = []
            for id in internal_ids:
                stations.append(
                    {
                        "internal_council_id": id,
                        "postcode": "",
                        "address": record["PollingStation"],
                        "location": location,
                        "polling_district_id": id,
                    }
                )
            return stations
