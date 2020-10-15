from django.core.exceptions import ObjectDoesNotExist
from addressbase.models import Address
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "S12000042"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Dundee"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["POLLING_DISTRICT"],
            "name": record["POLLING_DISTRICT"],
            "area": poly,
        }

    def get_address(self, uprn):
        ab = Address.objects.get(pk=uprn.lstrip("0"))
        return (ab.address, ab.postcode)

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        # Get full address from AddressBase if we can
        try:
            address, postcode = self.get_address(record["UPRN"])
        except ObjectDoesNotExist:
            address = record["NAME"]
            postcode = ""

        return {
            "internal_council_id": record["ID"],
            "address": address,
            "postcode": postcode,
            "location": location,
            "polling_district_id": record["POLLING_DISTRICT"],
        }
