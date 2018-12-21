from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000034"
    council_name = "Aberdeenshire"
    elections = ["local.aberdeenshire.2017-05-04", "parl.2017-06-08"]
