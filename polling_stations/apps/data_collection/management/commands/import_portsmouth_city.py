"""
Imports Portsmouth City Council
"""
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseJasonImporter

class Command(BaseJasonImporter):
    """
    Imports the polling station/district data
    """
    council_id     = 'E06000044'
    districts_name = 'PCC_Polling_2015.json'
    stations_name  = 'polling_stations2015.csv'
    # Work Aborted because the first export didn't contain either postcodes
    # or coordinates for stations
