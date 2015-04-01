"""
Import Islington
"""
from django.contrib.gis.geos import Point
import ffs

from data_collection.management.commands import BaseShpImporter

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
            'internal_council_id': record[7],
            'name': record[0],
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)
        return {
            'council': self.council,
            'internal_council_id': record.u_polldid,
            'postcode': record.postcode,
            'address': "\n".join([record.stat_title, record.stat_addr1, record.postcode]),
            'location': location
        }
    
    def import_polling_stations(self):
        base_folder = ffs.Path(self.base_folder_path)
        stations = base_folder/self.stations_name
        with stations.csv(header=True) as csv:
            for row in csv: 
                station_info = self.station_record_to_dict(row)
                self.add_polling_station(station_info)
