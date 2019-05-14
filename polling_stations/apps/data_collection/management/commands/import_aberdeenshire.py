from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000034"
    council_name = "Aberdeenshire"
    elections = ["europarl.2019-05-23"]
