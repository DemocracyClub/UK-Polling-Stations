from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 102/105 districts
due to incomplete/poor quality data
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000033"
    council_name = "Aberdeen City"
    elections = []

    def station_record_to_dict(self, record):
        # exclude duplicate/ambiguous codes
        if record[0] in ["DG0205", "DG0206", "CS1008"]:
            return None

        return super().station_record_to_dict(record)
