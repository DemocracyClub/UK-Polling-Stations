from data_collection.management.commands import BaseScotlandSpatialHubImporter

class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000010'
    council_name = 'East Lothian'
    elections = ['local.east-lothian.2017-05-04']
