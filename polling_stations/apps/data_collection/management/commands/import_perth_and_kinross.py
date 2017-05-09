from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 104/107 districts
due to incomplete/poor quality data
"""
class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000024'
    council_name = 'Perth and Kinross'
    elections = [
        'local.perth-and-kinross.2017-05-04',
        'parl.2017-06-08'
    ]
