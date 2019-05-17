from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000023"
    council_name = "Orkney Islands"
    elections = ["europarl.2019-05-23"]
