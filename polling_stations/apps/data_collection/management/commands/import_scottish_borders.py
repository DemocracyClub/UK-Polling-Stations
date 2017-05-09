from data_collection.management.commands import BaseScotlandSpatialHubImporter

class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000026'
    council_name = 'Scottish Borders'
    elections = [
        'local.scottish-borders.2017-05-04',
        'parl.2017-06-08'
    ]
