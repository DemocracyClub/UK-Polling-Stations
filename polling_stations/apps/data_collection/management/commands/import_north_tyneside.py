"""
Import North Tyneside
"""
import sys
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseShpImporter

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from North Tyneside
    """
    council_id     = 'E08000022'
    districts_name = 'NT_Polling_Districts_2014'
    stations_name  = 'NT_Polling_Stations_2015.csv'

    def district_record_to_dict(self, record):        
        return {
            'internal_council_id': record[4],
            'name': record[3],
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.mapeast), int(record.mapnorth), srid=self.srid)
        except ValueError:
            location = Point(float(record.mapeast), float(record.mapnorth), srid=self.srid)
        address = [
            record.place_pnam,
            record.place_add1,
            record.place_add2,
            record.place_add3,
            record.place_add4,
            record.place_add5            
        ]
        return {
            'internal_council_id': record.pd,
            'postcode'           : record.place_pcod,
            'address'            : "\n".join(address),
            'location'           : location
        }
    
