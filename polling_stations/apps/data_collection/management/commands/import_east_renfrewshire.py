from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000011"
    council_name = "East Renfrewshire"
    elections = ["europarl.2019-05-23"]
