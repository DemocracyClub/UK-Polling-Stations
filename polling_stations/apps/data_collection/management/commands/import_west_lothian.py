from data_collection.management.commands import BaseScotlandSpatialHubImporter
from data_collection.slugger import Slugger

"""
Note:
This importer provides coverage for 91/96 districts
due to incomplete/poor quality data

Districts LFL6B, LFL6L, LVL7X, LVL8Z and LVV3D missing polling place

"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000040"
    council_name = "West Lothian"
    elections = []
    station_map = {}
    seen_codes = set()

    def district_record_to_dict(self, record):
        if record[2] == self.council_name:
            station_slug = Slugger.slugify(record[3])
            if station_slug == "whitburn-bowling-club":
                station_slug = "whitburn-bowling-club-club"
            elif station_slug == "livingston-village-primary-school":
                station_slug = "livingston-village-primary"
            elif station_slug == "uphall-station-institute-hall":
                station_slug = "uphall-station-institue-hall"

            self.station_map.setdefault(station_slug, []).append(record[0])
            return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record[2] == self.council_name:
            try:
                station_slug = Slugger.slugify(record[3].split(",")[0])
                codes = self.station_map[station_slug]
            except KeyError:
                return None

            stations = []
            for code in codes:
                if code not in self.seen_codes:
                    self.seen_codes.add(code)
                    rec = {
                        "internal_council_id": code,
                        "postcode": "",
                        "address": record[3],
                    }
                    stations.append(rec)
            return stations
