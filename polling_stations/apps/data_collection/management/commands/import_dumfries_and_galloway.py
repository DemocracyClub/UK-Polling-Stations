from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000006"
    council_name = "Dumfries and Galloway"
    elections = ["europarl.2019-05-23"]
