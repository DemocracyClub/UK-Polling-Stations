from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000026"
    council_name = "Scottish Borders"
    elections = ["europarl.2019-05-23"]
