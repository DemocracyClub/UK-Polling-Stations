from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 87/107 districts
due to incomplete/poor quality data

Data at

http://gis-pkc.opendata.arcgis.com/datasets?q=polling&sort_by=-updatedAt
https://github.com/wdiv-scrapers/data/tree/master/S12000024

is also be worth a look, but at last check there were
some issues with overlapping polygons etc so could also be problematic
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000048"
    council_name = "Perth and Kinross"
    elections = ["parl.2017-06-08"]
