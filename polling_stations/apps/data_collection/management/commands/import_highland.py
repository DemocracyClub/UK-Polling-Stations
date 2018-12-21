from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000017"
    council_name = "Highland"
    elections = [
        "local.highland.2017-05-04",
        #'parl.2017-06-08'
    ]
