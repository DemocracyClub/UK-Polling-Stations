from data_collection.management.commands import BaseScotlandSpatialHubImporter
from data_collection.slugger import Slugger

"""
Note:
This importer provides coverage for 16/71 districts
due to incomplete/poor quality data
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000028"
    council_name = "South Ayrshire"
    elections = ["europarl.2019-05-23"]
    station_map = {}

    def district_record_to_dict(self, record):
        if record[2] == self.council_name:
            station_slug = Slugger.slugify(record[3])
            self.station_map.setdefault(station_slug, []).append(record[0])
            return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        try:
            station_slug = Slugger.slugify(record[3])
            codes = self.station_map[station_slug]
        except KeyError as e:
            return None

        stations = []
        for code in codes:
            rec = {"internal_council_id": code, "postcode": "", "address": record[3]}
            stations.append(rec)
        return stations
