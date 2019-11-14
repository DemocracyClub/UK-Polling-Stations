from addressbase.models import Address
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    council_id = "S12000048"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-PerthAndKinross"
    geom_type = "geojson"
    # districts file has station address and UPRN for district
    # parse the districts file twice
    stations_query = "districts"

    def geocode_from_uprn(self, uprn):
        uprn = str(uprn).lstrip("0").strip()
        ab_rec = Address.objects.get(uprn=uprn)
        return ab_rec.location

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["CODE"],
            "name": record["CODE"],
            "area": poly,
            "polling_station_id": record["CODE"],
        }

    def station_record_to_dict(self, record):
        try:
            location = self.geocode_from_uprn(record["UPRN"])
        except Address.DoesNotExist:
            location = None

        if record["CODE"] == "tba":
            return None

        return {
            "internal_council_id": record["CODE"],
            "address": record["ADDRESS"],
            "postcode": "",
            "location": location,
        }
