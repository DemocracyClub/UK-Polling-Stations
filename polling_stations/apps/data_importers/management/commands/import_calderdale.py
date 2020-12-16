from data_importers.geo_utils import fix_bad_polygons
from data_importers.management.commands import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    council_id = "E08000033"
    districts_name = "parl.2019-12-12/Version 2/Polling Districts Boundary 2019 Shape Files/POLLING_DISTRICTS.shp"
    stations_name = "parl.2019-12-12/Version 2/Polling stations shape files 2019-11-13 13-53-23/POLLING_STATIONS.shp"
    elections = ["parl.2019-12-12"]
    shp_encoding = "utf-8"

    def district_record_to_dict(self, record):
        code = record[0].strip()
        name = record[1].strip()
        return {"internal_council_id": code, "name": name, "polling_station_id": code}

    def station_record_to_dict(self, record):
        code = record[1].strip()
        address = record[0].strip()

        if code == "BP":
            code = "BM"

        if code == "" and address == "":
            return None

        return {"internal_council_id": code, "address": address, "postcode": ""}

    def post_import(self):
        fix_bad_polygons()
