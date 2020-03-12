import os
from data_collection.base_importers import ShpMixin
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter, ShpMixin):
    council_id = "E07000172"
    elections = ["2020-05-07"]

    # This one is a bit of a mish-mash
    # The stations are on GitHub
    srid = 4326
    scraper_name = "wdiv-scrapers/DC-PollingStations-Broxtowe"
    geom_type = "geojson"

    # but we need to import the districts from a file on S3
    districts_srid = 27700
    districts_name = "local.2019-05-02/Version 1/Polling_Districts_Split"
    districts_filetype = "shp"
    local_files = True

    def get_districts(self):
        districts_file = os.path.join(self.base_folder_path, self.districts_name)
        return self.get_data(self.districts_filetype, districts_file)

    def district_record_to_dict(self, record):
        return {
            "internal_council_id": record[6].strip(),
            "name": " - ".join([record[1].strip(), record[6].strip()]),
            "polling_station_id": record[6].strip(),
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )

        if record["ADDRESS"].lower().startswith(record["LABEL"].lower()):
            address = record["ADDRESS"]
        else:
            address = "\n".join([record["LABEL"], record["ADDRESS"]])

        return {
            "internal_council_id": record["POLL_DIST"],
            "address": address,
            "postcode": "",
            "location": location,
        }
