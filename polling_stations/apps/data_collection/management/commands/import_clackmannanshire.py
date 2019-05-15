from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000005"
    council_name = "Clackmannanshire"
    elections = ["europarl.2019-05-23"]
