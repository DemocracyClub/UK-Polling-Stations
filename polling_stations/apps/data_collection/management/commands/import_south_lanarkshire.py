from data_collection.management.commands import BaseScotlandSpatialHubImporter
from data_collection.slugger import Slugger

"""
Note:
This importer provides coverage for 172/173 districts
due to incomplete/poor quality data

No Polling Station for district SL114
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000029"
    council_name = "South Lanarkshire"
    elections = []
    station_map = {}

    def district_record_to_dict(self, record):
        if record[2] == self.council_name:
            station_slug = Slugger.slugify(record[3])
            self.station_map.setdefault(station_slug, []).append(record[0])
            return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record[2] == self.council_name:
            try:
                station_slug = Slugger.slugify(record[3])
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
