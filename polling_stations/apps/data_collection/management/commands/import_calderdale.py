from data_collection.geo_utils import fix_bad_polygons
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    council_id = "E08000033"
    districts_name = "local.2019-05-02/Version 1/Polling Districts 2019 Shp/POLLING_DISTRICTS_2019_region.shp"
    stations_name = "local.2019-05-02/Version 1/Polling Stations Shp 2019/POLLING_STATIONS_region.shp"
    elections = ["local.2019-05-02"]

    def parse_string(self, text):
        try:
            return text.strip().decode("utf-8")
        except AttributeError:
            return text.strip()

    def district_record_to_dict(self, record):
        code = self.parse_string(record[0])
        name = self.parse_string(record[1])
        return {"internal_council_id": code, "name": name, "polling_station_id": code}

    def station_record_to_dict(self, record):
        code = self.parse_string(record[1])
        address = self.parse_string(record[0])

        if code == "" and address == "":
            return None

        return {"internal_council_id": code, "address": address, "postcode": ""}

    def post_import(self):
        fix_bad_polygons()
