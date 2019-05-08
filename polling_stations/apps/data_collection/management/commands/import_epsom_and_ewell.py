from addressbase.models import Address
from uk_geo_utils.helpers import Postcode
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 27700
    districts_srid = 27700
    council_id = "E07000208"
    elections = ["europarl.2019-05-23"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-EpsomAndEwell"
    geom_type = "gml"
    # districts file has station address and UPRN for district
    # parse the districts file twice
    stations_query = "districts"

    def geocode_from_uprn(self, uprn, station_postcode):
        uprn = uprn.lstrip("0").strip()
        ab_rec = Address.objects.get(uprn=uprn)
        ab_postcode = Postcode(ab_rec.postcode)
        station_postcode = Postcode(station_postcode)
        if ab_postcode != station_postcode:
            print(
                "Using UPRN {uprn} for station ID but '{pc1}' != '{pc2}'".format(
                    uprn=uprn,
                    pc1=ab_postcode.with_space,
                    pc2=station_postcode.with_space,
                )
            )
        return ab_rec.location

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["wardcode"],
            "name": record["wardcode"],
            "area": poly,
            "polling_station_id": record["wardcode"],
        }

    def station_record_to_dict(self, record):
        postcode = " ".join(record["address"].split(" ")[-2:])
        try:
            location = self.geocode_from_uprn(record["uprn"].strip(), postcode)
        except Address.DoesNotExist:
            location = None

        return {
            "internal_council_id": record["wardcode"],
            "address": record["address"],
            "postcode": "",
            "location": location,
        }
