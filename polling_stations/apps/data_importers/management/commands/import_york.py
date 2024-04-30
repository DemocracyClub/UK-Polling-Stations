import re

from data_importers.github_importer import BaseGitHubImporter


def add_extra_codes(codes):
    # Grab an existing station code with the desired station info,
    # and add the missing code to the codes array, so another station is created.
    fixes = [
        # From https://www.northyorks.gov.uk/sites/default/files/2024-04/Situation%20of%20Polling%20Stations%20CYC%20-%20na.pdf
        ("YFB", "YHA2"),  # YHA2 -> HEWORTH WITHOUT COMMUNITY CENTRE
        ("YDE", "YDD"),  # YDD -> ST. MARGARET CLITHEROW CHURCH
        ("YKF", "BD"),  # BD -> JAMES HALL, CLIFTON PARISH CHURCH
        ("YLD", "YLC"),  # YLC -> STRENSALL AND TOWTHORPE VILLAGE HALL
        ("YGC", "YGB"),  # YGB -> ORCHARD PARK COMMUNITY CENTRE
        ("YKF", "YKE"),  # YKE -> JAMES HALL, CLIFTON PARISH CHURCH
        ("FF", "YFC"),  # YFC -> THE CENTRE @ BURNHOLME
        ("HG", "YCB"),  # YCB -> HESLINGTON VILLAGE MEETING ROOM
    ]
    for exists, missing in fixes:
        if exists in codes:
            codes.append(missing)

    return codes


class Command(BaseGitHubImporter):
    srid = 4326
    districts_srid = 4326
    council_id = "YOR"
    elections = ["2024-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-York"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        code = record["Code"].replace("/", "").strip()
        return {
            "internal_council_id": code,
            "name": "%s - %s" % (record["Ward"], code),
            "area": poly,
            "polling_station_id": code,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = re.split("[, ]", record["PollingDistrict"])
        codes = [code.replace("/", "").strip() for code in codes if code.strip()]
        codes = add_extra_codes(codes)
        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code.strip(),
                    "postcode": "",
                    "address": f'{record["PlaceName"]}/{record["Address"]}',
                    "location": location,
                    # "polling_district_id": code.strip(),
                }
            )
        return stations
