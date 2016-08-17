"""
Imports Spelthorne Council.
"""
import json 

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseCsvStationsKmlDistrictsImporter

class Command(BaseCsvStationsKmlDistrictsImporter):
    """
    Imports the Polling Station data from Spelthorne Council
    """
    council_id     = 'E07000213'
    districts_name = 'Polling_Districts.kmz'
    stations_name  = 'Polling_Stations.csv'
    elections      = ['parl.2015-05-07']

    def get_station_hash(self, record):
        return "-".join([
            record.polling_di,
            record.building,
            record.road,
            record.town_villa
        ])

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.point_x), int(record.point_y), srid=self.srid)
        except ValueError:
            location = Point(float(record.point_x), float(record.point_y), srid=self.srid)
        return {
            'internal_council_id': record.polling_di,
            'postcode': '',
            'address': "\n".join([record.building, record.road, record.town_villa]),
            'location': location,
            'polling_district_id': record.polling_di
        }
