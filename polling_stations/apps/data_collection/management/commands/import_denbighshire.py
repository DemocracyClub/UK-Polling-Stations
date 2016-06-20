"""
Import Denbighshire
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseAddressCsvImporter
from data_finder.helpers import geocode_point_only, PostcodeError

class Command(BaseAddressCsvImporter):
    """
    Imports the Polling Station data from Denbighshire
    """
    council_id      = 'W06000004'
    addresses_name  = 'PropertyPostCodePollingStationWebLookup-2016-02-09.CSV'
    stations_name   = 'PollingStations-2016-02-09.csv'
    csv_encoding    = 'latin-1'
    elections       = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):

        # format address
        address = "\n".join([
            record.pollingplaceaddress1,
            record.pollingplaceaddress2,
            record.pollingplaceaddress3,
            record.pollingplaceaddress4,
            record.pollingplaceaddress5,
            record.pollingplaceaddress6,
        ])
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")

        """
        No grid references were supplied,
        so attempt to derive a grid ref from postcode

        Unfortunately some of these postcodes cover
        quite large areas, so the postcode centroid may
        be some distance from the polling station :(
        """
        try:
            gridref = geocode_point_only(record.pollingplaceaddress7)
            location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
        except PostcodeError:
            location = None

        return {
            'internal_council_id': record.pollingplaceid,
            'postcode'           : record.pollingplaceaddress7,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):

        if record.propertynumber == '0':
            address = record.streetname
        else:
            address = '%s %s' % (record.propertynumber, record.streetname)

        return {
            'address'           : address,
            'postcode'          : record.postcode,
            'polling_station_id': record.pollingplaceid
        }
