"""
Import Dover
"""
from data_collection.management.commands import BaseShpShpImporter
from data_collection.google_geocoding_api_wrapper import GoogleGeocodingApiWrapper


class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Dover
    """
    council_id     = 'E07000108'
    districts_name = 'Dover_Polling_Boundaries'
    stations_name  = 'Dover_Polling_Stations.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):

        address = "\n".join([record[1]] + record[2].split(', '))

        # remove strange unicode char and replace with space
        postcode = record[3].replace('\xa0', ' ')
        postcode_parts = postcode.split(' ')

        # if postcode is invalid, attempt to fix it
        if len(postcode_parts[1]) == 2:
            gwrapper = GoogleGeocodingApiWrapper(address)
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
                postcode = ""

        return {
            'internal_council_id': record[0],
            'postcode'           : postcode,
            'address'            : address
        }
