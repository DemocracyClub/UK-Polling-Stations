"""
Import Gwynedd
"""
import shapefile
from time import sleep
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseShpShpImporter
from data_finder.helpers import geocode, PostcodeError

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Gwynedd Council

    Gwynedd have provided a single shp file with shapes
    for the boundaries and the polling station addresses
    embeddedin the attributes table. There are no points for
    the stations and no codes/ids for the districts or stations.

    We will parse the districts file twice, pull the station
    data from the attirbutes table and attempt to attach points
    by geocoding the station postcodes.
    """
    council_id = 'W06000002'
    districts_name = 'Catchments_Gwynedd'
    stations_name = 'Catchments_Gwynedd.shp'
    elections = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]
    district_count = 0
    station_count = 0

    def district_record_to_dict(self, record):
        # No IDs/codes were supplied, so we'll just assign each
        # district/station a sequential ID as we parse the file
        self.district_count = self.district_count + 1
        return {
            'internal_council_id': self.district_count,
            'name': record[0],
            'polling_station_id': self.district_count
        }

    def import_polling_stations(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.base_folder_path,
            self.stations_name)
        )
        for station in sf.shapeRecords():
            station_info = self.station_record_to_dict(station.record)
            if station_info is not None:
                station_info['council'] = self.council
                self.add_polling_station(station_info)

    def station_record_to_dict(self, record):
        # No IDs/codes were supplied, so we'll just assign each
        # district/station a sequential ID as we parse the file
        self.station_count = self.station_count + 1

        # No grid references were supplied,
        # so attempt to derive a grid ref from postcode
        sleep(1.3) # ensure we don't hit mapit's usage limit
        try:
            gridref = geocode(record[6])
            location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
        except PostcodeError:
            location = None

        # format address
        address_parts = []
        for i in range(0,6):
            if record[i].strip():
                address_parts.append(record[i].strip())
        address = "\n".join(address_parts)

        return {
            'internal_council_id': self.station_count,
            'postcode': record[6],
            'address': address,
            'location': location
        }
