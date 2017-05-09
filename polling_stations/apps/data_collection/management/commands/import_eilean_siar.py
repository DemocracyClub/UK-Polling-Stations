from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 45/47 districts
due to incomplete/poor quality data
"""
class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000013'
    council_name = 'Eilean Siar'
    elections = [
        'local.eilean-siar.2017-05-04',
        'parl.2017-06-08'
    ]

    def station_record_to_dict(self, record):
        # bless 'em
        record[1] = self.parse_string(record[1]).replace('O', '0')

        # exclude duplicate district code
        if record[1] == 'E09E':
            return None

        return super().station_record_to_dict(record)
