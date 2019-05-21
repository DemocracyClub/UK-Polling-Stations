import os
from data_collection.base_importers import CsvMixin
from data_collection.github_importer import BaseGitHubImporter
from data_finder.helpers import geocode_point_only, PostcodeError


class Command(BaseGitHubImporter, CsvMixin):

    srid = 27700
    districts_srid = 27700
    council_id = "E07000077"
    elections = ["europarl.2019-05-23"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Uttlesford"
    geom_type = "geojson"
    # districts file has station address and UPRN for district
    # parse the districts file twice
    stations_query = "districts"
    # ..and then the postcodes for the polling stations
    # are in a CSV file on S3
    local_files = True
    csv_encoding = "utf-8"
    csv_delimiter = ","

    def pre_import(self):
        postcodes_file = os.path.join(
            self.base_folder_path,
            "europarl.2019-05-23/Version 1/Uttlesford Postcodes.csv",
        )
        postcodes = self.get_data("csv", postcodes_file)
        self.postcodes = {pc.district_code: pc.postcode for pc in postcodes}

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["PD_ID"],
            "name": record["PD_ID"],
            "area": poly,
            "polling_station_id": record["PD_ID"],
        }

    def station_record_to_dict(self, record):
        postcode = self.postcodes[record["PD_ID"]]

        try:
            location_data = geocode_point_only(postcode)
            location = location_data.centroid
        except PostcodeError:
            location = None

        return {
            "internal_council_id": record["PD_ID"],
            "address": record["Polling_St"],
            "postcode": postcode,
            "location": location,
        }
