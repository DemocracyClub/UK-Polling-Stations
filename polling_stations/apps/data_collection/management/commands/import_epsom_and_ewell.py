from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 27700
    districts_srid = 27700
    council_id = "E07000208"
    elections = ["local.2019-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-EpsomAndEwell"
    geom_type = "gml"
    duplicate_districts = set()

    def pre_import(self):
        self.find_duplicate_districts()

    def find_duplicate_districts(self):
        # identify any district codes which appear
        # more than once (with 2 different polygons)
        # We do not want to import these.
        seen = set()
        districts = self.get_districts()
        for district in districts:
            if str(district["wardcode"]) in seen:
                self.duplicate_districts.add(str(district["wardcode"]))
            seen.add(str(district["wardcode"]))

    def get_station_hash(self, record):
        # handle exact dupes on code/address
        return "-".join([record["wardname"], record["uprn"]])

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        if record["wardcode"] in self.duplicate_districts:
            return None
        else:
            return {
                "internal_council_id": record["wardcode"],
                "name": record["wardcode"],
                "area": poly,
                "polling_station_id": record["wardcode"],
            }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        return {
            "internal_council_id": record["wardname"],
            "postcode": "",
            "address": record["address"],
            "location": location,
        }
