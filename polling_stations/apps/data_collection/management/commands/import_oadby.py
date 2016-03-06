"""
Import Oadby & Wigston
"""
from data_collection.management.commands import BaseShpShpImporter
from data_collection.google_geocoding_api_wrapper import (
    GoogleGeocodingApiWrapper,
    PostcodeNotFoundException
)


class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Oadby & Wigston
    """
    council_id     = 'E07000135'
    districts_name = 'Polling Districts'
    stations_name  = 'Polling_Stations.shp'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'name': record[1],
        }

    def station_record_to_dict(self, record):

        # ignore proposed stations
        if record[0] == 'Current':

            address = self.format_address(record)
            postcode = record[9].strip()

            # if postcode is missing, attempt to attach it
            if not postcode:
                gwrapper = GoogleGeocodingApiWrapper(address, self.council_id, 'DIS')
                try:
                    postcode = gwrapper.address_to_postcode()
                except PostcodeNotFoundException:
                    postcode = ''

            return {
                'internal_council_id': record[15],
                'postcode'           : postcode,
                'address'            : address
            }

        else:
            return None

    def format_address(self, record):

        name = record[1]

        if record[2] != 0:
            street_address = str(record[2]) + ' ' + record[5]
        else:
            street_address = record[5]

        if isinstance(record[4], bytes):
            building = str(record[4], encoding='UTF-8').strip()
        else:
            building = record[4].strip()

        if isinstance(record[7], bytes):
            locality = str(record[7], encoding='UTF-8').strip()
        else:
            locality = record[7].strip()

        town = record[6]

        address = "\n".join([
            name,
            building,
            street_address,
            locality,
            town
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")

        return address
