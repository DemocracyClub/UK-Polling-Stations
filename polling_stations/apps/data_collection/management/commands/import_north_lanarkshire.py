from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 173/174 districts
due to incomplete/poor quality data
"""
class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000044'
    council_name = 'North Lanarkshire'
    elections = [
        'local.north-lanarkshire.2017-05-04',
        'parl.2017-06-08'
    ]

    def station_record_to_dict(self, record):
        # clean up codes
        record[1] = self.parse_string(record[1]).replace(' ', '').upper()
        return super().station_record_to_dict(record)

    def district_record_to_dict(self, record):
        # clean up codes
        record[0] = self.parse_string(record[0]).replace(' ', '').upper()
        return super().district_record_to_dict(record)
