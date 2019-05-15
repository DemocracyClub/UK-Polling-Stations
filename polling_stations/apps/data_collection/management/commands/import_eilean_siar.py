from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 45/47 districts
due to incomplete/poor quality data
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000013"
    council_name = "Eilean Siar"
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):
        record[0] = self.parse_string(record[0]).replace("O", "0")

        # exclude duplicate district code
        if record[0] == "E09E":
            return None

        return super().station_record_to_dict(record)
