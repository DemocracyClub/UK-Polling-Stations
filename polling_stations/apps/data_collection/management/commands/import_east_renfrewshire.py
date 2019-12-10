from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000011"
    council_name = "East Renfrewshire"
    elections = ["parl.2019-12-12"]
