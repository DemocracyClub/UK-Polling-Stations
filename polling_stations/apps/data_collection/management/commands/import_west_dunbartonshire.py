from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000039"
    council_name = "West Dunbartonshire"
    elections = ["local.west-dunbartonshire.2017-05-04", "parl.2017-06-08"]
