from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 66/81 districts
due to incomplete/poor quality data
"""
class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000008'
    council_name = 'East Ayrshire'
    elections = ['local.east-ayrshire.2017-05-04']

    def station_record_to_dict(self, record):
        # exclude duplicate district code
        if str(record[1]).strip() == 'E706':
            return None
        return super().station_record_to_dict(record)
