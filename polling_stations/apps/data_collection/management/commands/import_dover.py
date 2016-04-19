"""
Import Dover
"""
import shapefile
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseShpShpImporter
from data_collection.google_geocoding_api_wrapper import (
    GoogleGeocodingApiWrapper,
    PostcodeNotFoundException
)

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Dover
    """
    council_id     = 'E07000108'
    districts_name = 'Dover_Polling_Boundaries'
    stations_name  = 'Dover_Polling_Stations.shp'
    elections      = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name':                record[1],
            'polling_station_id':  record[1][:3]
        }

    # station_record_to_dicts() returns an array of dicts in this script
    def import_polling_stations(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.base_folder_path,
            self.stations_name
            ))
        for station in sf.shapeRecords():
            station_info = self.station_record_to_dicts(station.record)
            if station_info is not None:
                for station_record in station_info:
                    station_record['location'] = Point(
                        *station.shape.points[0],
                        srid=self.get_srid())
                    self.add_polling_station(station_record)

    def station_record_to_dicts(self, record):

        address = "\n".join([record[1]] + record[2].split(', '))

        # remove strange unicode char and replace with space
        postcode = record[3].replace('\xa0', ' ')
        postcode_parts = postcode.split(' ')

        # if postcode is invalid, attempt to fix it
        if len(postcode_parts[1]) == 2:
            gwrapper = GoogleGeocodingApiWrapper(address, self.council_id, 'DIS')
            try:
                suggested_postcode = gwrapper.address_to_postcode()
                """
                In this case we have a partial postcode we can use to verify, so:
                If the first 6 characters of the suggested postcode match
                with the partial postcode we already have then accept the suggestion
                otherwise, discard both and insert blank postcode
                """
                if suggested_postcode[:-1] == postcode:
                    postcode = suggested_postcode
                else:
                    postcode = ''
            except PostcodeNotFoundException:
                postcode = ''

        """
        In this data, sometimes a single polling station serves several
        districts. For simplicity, if record[4] is something like "AA4, AD3" 
        return the same polling station address/point twice with 2 different IDs
        """
        internal_ids = record[4].split(", ")
        if (len(internal_ids) == 2):
            return [
                { 'internal_council_id': internal_ids[0],
                  'postcode'           : postcode,
                  'address'            : address },
                { 'internal_council_id': internal_ids[1],
                  'postcode'           : postcode,
                  'address'            : address }
            ]
        else:
            return [{
                'internal_council_id': internal_ids[0],
                'postcode'           : postcode,
                'address'            : address
            }]
