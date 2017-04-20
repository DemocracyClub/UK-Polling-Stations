from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 32/39 districts
due to incomplete/poor quality data
"""
class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000010'
    council_name = 'East Lothian'
    elections = ['local.east-lothian.2017-05-04']
    seen_stations = set()

    def station_record_to_dict(self, record):
        code = self.parse_string(record[1])
        # code 'EL7H' appears twice with the same point
        # and (roughly) the same address
        # ensure we only try to import it once
        if code in self.seen_stations:
            return None
        self.seen_stations.add(code)
        return super().station_record_to_dict(record)
