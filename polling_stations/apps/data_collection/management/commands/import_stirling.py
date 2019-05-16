from data_collection.management.commands import BaseScotlandSpatialHubImporter
from data_collection.slugger import Slugger

"""
Note:
This importer provides coverage for 48/51 districts
due to incomplete/poor quality data

Station (Murray Hall) for District SC420 not in source data.
Station (Aberfoyle Primary School) for District SS165 not in source data.
Station (Stirling Indoor Bowling Centre) for District SS440 not in source data.
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000030"
    council_name = "Stirling"
    elections = ["europarl.2019-05-23"]
    station_map = {}
    seen_codes = set()

    def district_record_to_dict(self, record):
        if record[2] == self.council_name:
            station_slug = Slugger.slugify(record[3])
            if station_slug == "thornhill-village-hall":
                station_slug = "thornhill-community-hall"
            elif station_slug == "john-mclintock-hall":
                station_slug = "mclintock-hall"
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
