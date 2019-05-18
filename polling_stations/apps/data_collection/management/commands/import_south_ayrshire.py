from data_collection.management.commands import BaseScotlandSpatialHubImporter
from data_collection.slugger import Slugger

"""
Note:
This importer provides coverage for 55/71 districts
due to incomplete/poor quality data
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000028"
    council_name = "South Ayrshire"
    elections = ["europarl.2019-05-23"]
    station_map = {}

    def district_record_to_dict(self, record):
        if record[2] == self.council_name:
            name_postcode = f"{record[3].split(',')[0]} {record[3].split(',')[-1]}"
            station_slug = Slugger.slugify(name_postcode)
            self.station_map.setdefault(station_slug, []).append(record[0])
            return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record[2] == self.council_name:
            try:
                name_postcode = f"{record[3].split(',')[0]} {record[3].split(',')[-1]}"
                station_slug = Slugger.slugify(name_postcode)
                codes = self.station_map[station_slug]
            except KeyError:
                return None

            stations = []
            for code in codes:
                rec = {
                    "internal_council_id": code,
                    "postcode": "",
                    "address": record[3],
                }
                stations.append(rec)
            return stations
