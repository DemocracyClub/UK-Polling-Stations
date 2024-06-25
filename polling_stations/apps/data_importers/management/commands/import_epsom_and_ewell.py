from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 27700
    districts_srid = 27700
    council_id = "EPS"
    elections = ["2024-07-04"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-EpsomAndEwell"
    geom_type = "gml"
    seen = set()

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        if record["id"] in [
            "pollingdistricts.33",
            "pollingdistricts.38",
            "pollingdistricts.50",
        ]:
            return None
        return {
            "internal_council_id": record["district"],
            "name": record["district"],
            "area": poly,
        }

    def station_record_to_dict(self, record):
        postcode = " ".join(record["address"].split(" ")[-2:])
        if len(postcode) > 8:
            postcode = ""
        point = self.extract_geometry(record, self.geom_type, self.get_srid())

        if (record["district"], postcode) in self.seen:
            return None

        self.seen.add((record["district"], postcode))
        return {
            "internal_council_id": record["psnumber"],
            "polling_district_id": record["district"],
            "address": record["address"],
            "postcode": postcode,
            "location": point,
        }
