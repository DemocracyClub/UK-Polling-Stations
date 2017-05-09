from data_collection.management.commands import BaseScotlandSpatialHubImporter

class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000005'
    council_name = 'Clackmannanshire'
    elections = [
        'local.clackmannanshire.2017-05-04',
        'parl.2017-06-08'
    ]
