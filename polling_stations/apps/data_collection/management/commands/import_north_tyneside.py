"""
Import North Tyneside
"""
import sys
from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsShpDistrictsImporter

class Command(BaseCsvStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from North Tyneside
    """
    council_id     = 'E08000022'
    districts_name = 'NT_Polling_Districts_2014'
    stations_name  = 'NT_Polling_Stations_2015.csv'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[-1],
            'name': "%s - %s" % (record[3], record[-1]),
            'polling_station_id': record[-1]
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.mapeast), int(record.mapnorth), srid=self.srid)
        except ValueError:
            location = Point(float(record.mapeast), float(record.mapnorth), srid=self.srid)
        address_parts = [
            record.place_pnam,
            record.place_add1,
            record.place_add2,
            record.place_add3,
            record.place_add4,
            record.place_add5
        ]
        address = "\n".join(address_parts).strip()

        """
        In this file, some of the polling stations have a grid ref but no address
        Insert them in the DB with address = "Address not supplied"
        on the basis we can still provide directions to the grid ref.
        """
        if address == '' and record.place_pcod == '':
            address = "Address not supplied"

        return {
            'internal_council_id': record.pd,
            'postcode'           : record.place_pcod,
            'address'            : address,
            'location'           : location
        }
