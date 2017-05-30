from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 87/107 districts
due to incomplete/poor quality data
"""
class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000024'
    council_name = 'Perth and Kinross'
    elections = [
        'parl.2017-06-08'
    ]
