"""
Import East Riding
"""
import os
from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseCsvStationsShpDistrictsImporter,
    CsvHelper
)

class Command(BaseCsvStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from East Riding of Yorkshire Council
    """
    council_id     = 'E06000011'
    districts_name = 'Polling_Districts.shpn'
    stations_name  = 'FOI6287_polling-stations.csv'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'name': record[2],
            'polling_station_id': record[1]
        }

    # station_record_to_dicts() returns an array of dicts in this script
    def import_polling_stations(self):
        stations_file = os.path.join(self.base_folder_path, self.stations_name)

        helper = CsvHelper(stations_file, self.csv_encoding)
        data = helper.parseCsv()
        for row in data:
            stations = self.station_record_to_dicts(row)
            for station in stations:
                if 'council' not in station:
                    station['council'] = self.council

                self.add_polling_station(station)

    def station_record_to_dicts(self, record):

        try:
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)
        addr = [record.name_of_station.strip()]
        addr += [x.strip() for x in record.address.split(',')[:-1]]

        postcode_parts = record.address.split(',')[-1].split(' ')
        postcode = "%s %s" % (postcode_parts[-2], postcode_parts[-1])

        """
        In this data, sometimes a single polling station serves several
        districts. For simplicity, if record.code is something like "CA, CB, CE"
        return the same polling station address/point multiple times with different IDs
        """
        internal_ids = record.code.split(", ")
        if (len(internal_ids) == 1):
            return [{
                'internal_council_id': record.code,
                'postcode'           : postcode,
                'address'            : "\n".join(addr),
                'location'           : location
            }]
        else:
            stations = []
            for id in internal_ids:
                stations.append({
                    'internal_council_id': id,
                    'postcode'           : postcode,
                    'address'            : "\n".join(addr),
                    'location'           : location
                })
            return stations
