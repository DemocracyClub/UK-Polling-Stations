import re
from data_collection.github_importer import BaseGitHubImporter
from data_collection.addresshelpers import format_polling_station_address


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E06000023"
    elections = ["europarl.2019-05-23"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Bristol"
    geom_type = "geojson"
    stations_query = "stations_opend"
    districts_query = "districts_opend"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["polling_dist_id"].strip(),
            "name": record["polling_dist_id"].strip(),
            "area": poly,
            "polling_station_id": record["polling_dist_id"].strip(),
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
        stations = stations.replace("Used bu", "")
        stations = stations.replace("Used for", "")
        codes = []
        if "and" in stations:
            codes = re.split("and|,", stations)
        elif "amd" in stations:
            codes = re.split("amd|,", stations)
        elif "&" in stations:
            codes = re.split("&|,", stations)
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
                record["pao"] if record["pao"] else "",
                record["street"] if record["street"] else "",
                record["locality"] if record["locality"] else "",
            ]
        )
        postcode = ""
        if record["postcode"]:
            postcode = record["postcode"].strip()

        if record["dual_stn"]:
            codes = self.extract_codes(record["dual_stn"])
        else:
            codes = [record["polling_district"].strip()]

        if (
            record["pao"] == "Stockwood Library"
            and record["polling_district"].strip() == "STWD"
        ):
            codes = ["STWE"]

        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code,
                    "postcode": postcode,
                    "address": address,
                    "location": location,
                }
            )
        return stations
