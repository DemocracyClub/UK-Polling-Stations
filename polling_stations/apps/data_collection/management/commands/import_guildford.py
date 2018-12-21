from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 27700
    districts_srid = 27700
    council_id = "E07000209"
    elections = ["parl.2017-06-08"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Guildford"
    geom_type = "gml"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["register"],
            "name": record["pollingdistrictname"],
            "area": poly,
            "polling_station_id": record["register"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        return {
            "internal_council_id": record["register"],
            "postcode": "",
            "address": "%s\n%s" % (record["pollingplace"], record["thoroughfare_name"]),
            "location": location,
        }
