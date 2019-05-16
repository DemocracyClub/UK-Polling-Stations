from data_collection.management.commands import BaseScotlandSpatialHubImporter
from data_collection.slugger import Slugger

"""
Note:
This importer provides coverage for 103/107 districts
due to incomplete/poor quality data

Station RAILWAY STAFF CLUB, PERTH has no districts assigned to it.
Districts Wellshill and Fairfield are assinged to
Fairfield Neighbourhood Centre, Perth. But this station is  not in the polling
stations source file. The RAILWAY STAFF CLUB could be correct for these.
District Hoole has polling place 'Inchture Village Hall, Kinrossie' aassigned
which is ambiguous becasue Kinrossie and Inchture are not the same place and
District Inchture has 'Inchture Village Hall, Inchture' which looks correct.
District East Ruthenfield has no polling station due to an abscence of electors.


Data at
http://gis-pkc.opendata.arcgis.com/datasets?q=polling&sort_by=-updatedAt
https://github.com/wdiv-scrapers/data/tree/master/S12000024

is also be worth a look, but at last check there were
some issues with overlapping polygons etc so could also be problematic
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000048"
    council_name = "Perth and Kinross"
    elections = ["europarl.2019-05-23"]
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
                if station_slug == "pitcairngreen-village-hall-pitcairngreen":
                    station_slug = "pitcairngreen-village-hall-almondbank"

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
