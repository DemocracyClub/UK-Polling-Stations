from data_collection.management.commands import BaseScotlandSpatialHubImporter

class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000020'
    council_name = 'Moray'
    elections = [
        'local.moray.2017-05-04',
        'parl.2017-06-08'
    ]
