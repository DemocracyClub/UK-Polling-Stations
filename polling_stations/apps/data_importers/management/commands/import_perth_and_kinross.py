from addressbase.models import Address
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    council_id = "PKN"
    elections = ["2021-05-06"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-PerthAndKinross"
    geom_type = "geojson"

    def geocode_from_uprn(self, uprn):
        uprn = str(uprn).lstrip("0").strip()
        ab_rec = Address.objects.get(uprn=uprn)
        return ab_rec.location

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        if record["PPD_CODE"] == "tba":
            return None

        return {
            "internal_council_id": record["PPD_CODE"],
            "name": record["PPD_CODE"],
            "area": poly,
            "polling_station_id": record["PPD_CODE"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("districts")
        )

        address = f'{record["POLL_PLACE"]}, {record["PPD_NAMES"]}'
        codes = record["PPD_CODES"].split(",")
        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code.strip(),
                    "address": address,
                    "postcode": "",
                    "location": location,
                }
            )
        return stations
