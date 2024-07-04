import re

from data_importers.addresshelpers import format_polling_station_address
from data_importers.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "BST"
    elections = ["2024-07-04"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Bristol"
    geom_type = "geojson"
    stations_query = "stations"
    districts_query = "districts"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["POLLING_DIST_ID"].strip(),
            "name": record["POLLING_DIST_NAME"].strip(),
            "area": poly,
            "polling_station_id": record["POLLING_DIST_ID"].strip(),
        }

    def extract_codes(self, text):
        """
        Bristol's data does tell us about stations that serve multiple stations
        but not in a very nice way e.g:

        CEND and CENB
        SGWD & SGWB
        Used by CLIB and CLIA
        Used by REDC amd REDG
        Used by BEDA & BEDC
        STWB, STWA1 and STWA2

        Attempt to make sense of this
        """
        stations = text
        stations = stations.replace("Used by", "")
        stations = stations.replace("Used for", "")
        codes = []
        if "and" in stations:
            codes = re.split("and|,", stations)
        elif "amd" in stations:
            codes = re.split("amd|,", stations)
        elif "&" in stations:
            codes = re.split("[&,]", stations)
        else:
            raise ValueError("Could not parse 'DUAL_STN' field: %s" % text)

        codes = [code.strip() for code in codes]

        if len(codes) < 2:
            raise ValueError("Could not parse 'DUAL_STN' field: %s" % text)

        return codes

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        address = format_polling_station_address(
            [
                record["PAO"] if record["PAO"] else "",
                record["STREET"] if record["STREET"] else "",
                record["LOCALITY"] if record["LOCALITY"] else "",
            ]
        )
        postcode = ""
        if record["POSTCODE"]:
            postcode = record["POSTCODE"].strip()

        if record["DUAL_STN"] and record["DUAL"].lower() != "no":
            codes = self.extract_codes(record["DUAL_STN"])
        else:
            codes = [record["POLLING_DISTRICT"].strip()]

        stations = []
        for code in codes:
            if code in ("LAWK", "LAWL", "LAWJ", "LAWG"):
                postcode = "BS2 0LT"
            stations.append(
                {
                    "internal_council_id": code,
                    "postcode": postcode,
                    "address": address,
                    "location": location,
                }
            )
        return stations
