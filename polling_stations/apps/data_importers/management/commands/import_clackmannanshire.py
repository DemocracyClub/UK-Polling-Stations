from data_importers.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000005"
    council_name = "Clackmannanshire"
    elections = ["parl.2019-12-12"]
