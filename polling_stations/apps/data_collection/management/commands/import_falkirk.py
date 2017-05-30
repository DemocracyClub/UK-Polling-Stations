from data_collection.management.commands import BaseScotlandSpatialHubImporter

class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000014'
    council_name = 'Falkirk'
    elections = [
        'parl.2017-06-08'
    ]
