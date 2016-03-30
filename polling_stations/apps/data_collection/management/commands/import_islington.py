"""
Import Islington
"""
import os
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseShpImporter, CsvHelper

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Islington Council
    """
    council_id = 'E09000019'
    districts_name = 'POLLING_AREA'
    stations_name = 'PollingStations.csv'

    def district_record_to_dict(self, record):
        return {
            'council': self.council,
            'internal_council_id': record[3],
            'name': record[0],
            'polling_station_id': record[3]
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)
        return {
            'council': self.council,
            'internal_council_id': record.rec_pd,
            'postcode': record.postcode,
            'address': "\n".join([record.stat_title, record.stat_addr1]),
            'location': location,
            'polling_district_id': record.rec_pd
        }
    
    def import_polling_stations(self):
        stations = os.path.join(self.base_folder_path, self.stations_name)
        helper = CsvHelper(stations)
        data = helper.parseCsv()
        for row in data:
            station_info = self.station_record_to_dict(row)
            self.add_polling_station(station_info)
