from data_importers.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000019"
    council_name = "Midlothian"
    elections = ["parl.2019-12-12"]
