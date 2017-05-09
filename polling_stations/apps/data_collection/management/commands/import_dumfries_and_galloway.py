from data_collection.management.commands import BaseScotlandSpatialHubImporter

class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000006'
    council_name = 'Dumfries and Galloway'
    elections = [
        'local.dumfries-and-galloway.2017-05-04',
        'parl.2017-06-08'
    ]
